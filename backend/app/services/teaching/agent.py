import asyncio
import json
import logging
import uuid
from collections.abc import AsyncGenerator
from datetime import datetime, timezone

from app.services.ai_client import chat_completion_stream
from app.services.teaching.assessment import assess_response
from app.services.teaching.prompts import (
    EXPLAIN_SYSTEM_PROMPT,
    CHECK_SYSTEM_PROMPT,
    DEEPEN_SYSTEM_PROMPT,
    ADVANCE_SYSTEM_PROMPT,
)

logger = logging.getLogger(__name__)

# In-memory registry of active sessions
_session_registry: dict[str, "TeachingAgent"] = {}


def get_agent(session_id: str) -> "TeachingAgent | None":
    return _session_registry.get(session_id)


def register_agent(session_id: str, agent: "TeachingAgent") -> None:
    _session_registry[session_id] = agent


def remove_agent(session_id: str) -> None:
    _session_registry.pop(session_id, None)


class TeachingAgent:
    def __init__(
        self,
        session_id: str,
        section_id: str,
        knowledge_points: list[dict],
        section_title: str,
    ):
        self.session_id = session_id
        self.section_id = section_id
        self.section_title = section_title
        # Each KP is {"id": str, "concept": str, "explanation": str, "difficulty": int}
        self.knowledge_points = knowledge_points
        self.current_kp_index = 0
        self.state = "idle"
        self.last_question: str = ""

        # For pausing/resuming when waiting for user input
        self._user_event = asyncio.Event()
        self._user_message: str | None = None

    def receive_message(self, content: str) -> None:
        """Called by the POST /message endpoint to deliver user input."""
        self._user_message = content
        self._user_event.set()

    async def _wait_for_user(self) -> str:
        """Block until the user sends a message."""
        self._user_event.clear()
        self._user_message = None
        await self._user_event.wait()
        msg = self._user_message or ""
        self._user_message = None
        return msg

    async def _stream_ai(self, prompt: str) -> AsyncGenerator[dict, None]:
        """Stream an AI response, yielding SSE token events. Returns full text via stream_complete."""
        collected = []
        async for chunk in chat_completion_stream(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
        ):
            collected.append(chunk)
            yield {"event": "token", "data": chunk}

        full_text = "".join(collected)
        yield {"event": "stream_complete", "data": json.dumps({"content": full_text})}

    async def event_generator(self) -> AsyncGenerator[dict, None]:
        """Main loop — yields SSE event dicts for the entire study session.

        Flow per KP:
        1. Wait for user to select a KP (or auto-start first one)
        2. EXPLAIN: stream AI illustration
        3. CHECK: stream AI question, then wait for user answer
        4. EVALUATE: assess answer, send feedback
        5. If quality < 3: DEEPEN then re-CHECK
        6. Emit kp_complete, then wait for next KP selection
        """
        try:
            while self.current_kp_index < len(self.knowledge_points):
                if self.current_kp_index > 0:
                    # Wait for user to click next KP
                    self.state = "idle"
                    yield {"event": "waiting_advance", "data": json.dumps({
                        "current_kp_index": self.current_kp_index - 1,
                    })}
                    user_input = await self._wait_for_user()
                    # User can send "advance:<index>" to jump to a specific KP
                    if user_input.startswith("advance:"):
                        try:
                            target = int(user_input.split(":")[1])
                            if 0 <= target < len(self.knowledge_points):
                                self.current_kp_index = target
                        except (ValueError, IndexError):
                            pass

                kp = self.knowledge_points[self.current_kp_index]

                # --- EXPLAIN (illustrate) ---
                self.state = "explain"
                yield {"event": "state_change", "data": json.dumps({
                    "state": "explain",
                    "current_kp_index": self.current_kp_index,
                })}

                prompt = EXPLAIN_SYSTEM_PROMPT.format(
                    concept=kp["concept"],
                    explanation=kp["explanation"],
                    difficulty=kp["difficulty"],
                    section_title=self.section_title,
                )
                async for event in self._stream_ai(prompt):
                    yield event

                # --- CHECK ---
                self.state = "check"
                yield {"event": "state_change", "data": json.dumps({
                    "state": "check",
                    "current_kp_index": self.current_kp_index,
                })}

                check_prompt = CHECK_SYSTEM_PROMPT.format(
                    concept=kp["concept"],
                    explanation=kp["explanation"],
                )
                async for event in self._stream_ai(check_prompt):
                    if event["event"] == "stream_complete":
                        self.last_question = json.loads(event["data"])["content"]
                    yield event

                # Wait for user answer
                user_answer = await self._wait_for_user()
                yield {"event": "user_answer", "data": json.dumps({"content": user_answer})}

                # --- EVALUATE ---
                self.state = "evaluate"
                yield {"event": "state_change", "data": json.dumps({
                    "state": "evaluate",
                    "current_kp_index": self.current_kp_index,
                })}

                result = await assess_response(
                    student_response=user_answer,
                    concept=kp["concept"],
                    explanation=kp["explanation"],
                    question=self.last_question,
                )
                yield {"event": "feedback", "data": json.dumps({
                    "quality": result.quality,
                    "feedback": result.feedback,
                })}

                if result.quality < 3:
                    # --- DEEPEN ---
                    self.state = "deepen"
                    yield {"event": "state_change", "data": json.dumps({
                        "state": "deepen",
                        "current_kp_index": self.current_kp_index,
                    })}

                    deepen_prompt = DEEPEN_SYSTEM_PROMPT.format(
                        concept=kp["concept"],
                        explanation=kp["explanation"],
                    )
                    async for event in self._stream_ai(deepen_prompt):
                        yield event

                    # Re-check
                    self.state = "check"
                    yield {"event": "state_change", "data": json.dumps({
                        "state": "check",
                        "current_kp_index": self.current_kp_index,
                    })}

                    check_prompt2 = CHECK_SYSTEM_PROMPT.format(
                        concept=kp["concept"],
                        explanation=kp["explanation"],
                    )
                    async for event in self._stream_ai(check_prompt2):
                        if event["event"] == "stream_complete":
                            self.last_question = json.loads(event["data"])["content"]
                        yield event

                    user_answer2 = await self._wait_for_user()
                    yield {"event": "user_answer", "data": json.dumps({"content": user_answer2})}

                    result2 = await assess_response(
                        student_response=user_answer2,
                        concept=kp["concept"],
                        explanation=kp["explanation"],
                        question=self.last_question,
                    )
                    yield {"event": "feedback", "data": json.dumps({
                        "quality": result2.quality,
                        "feedback": result2.feedback,
                    })}

                # --- KP COMPLETE ---
                yield {"event": "kp_complete", "data": json.dumps({
                    "kp_index": self.current_kp_index,
                })}
                self.current_kp_index += 1

            # Session complete
            yield {"event": "done", "data": ""}

        except Exception as e:
            logger.error("Teaching agent error for session %s: %s", self.session_id, e)
            yield {"event": "error", "data": str(e)}
        finally:
            remove_agent(self.session_id)
