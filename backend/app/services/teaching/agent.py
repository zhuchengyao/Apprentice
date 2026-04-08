import asyncio
import json
import logging
import os
import re
from collections.abc import AsyncGenerator, Callable, Awaitable
from typing import Optional

from app.config import settings
from app.services.ai_client import chat_completion_stream, build_image_content_blocks
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
    """Command-driven teaching agent.

    Instead of a rigid sequential flow, the agent waits for user commands:
      - "select:<index>"  → switch to that KP, run explain+check if needed
      - any other text     → treat as answer to the current KP's question

    A KP is considered mastered once the user answers its question.
    Users can freely jump between KPs at any time.
    """

    def __init__(
        self,
        session_id: str,
        section_id: str,
        knowledge_points: list[dict],
        section_title: str,
        save_illustration_cb: Optional[Callable[[str, str], Awaitable[None]]] = None,
        save_question_cb: Optional[Callable[[str, str], Awaitable[None]]] = None,
        save_mastery_cb: Optional[Callable[[str], Awaitable[None]]] = None,
        save_state_cb: Optional[Callable[[str, int], Awaitable[None]]] = None,
        section_image_paths: Optional[list[str]] = None,
    ):
        self.session_id = session_id
        self.section_id = section_id
        self.section_title = section_title
        self.knowledge_points = knowledge_points
        self.current_kp_index = 0
        self.state = "idle"
        self._save_illustration_cb = save_illustration_cb
        self._save_question_cb = save_question_cb
        self._save_mastery_cb = save_mastery_cb
        self._save_state_cb = save_state_cb
        self._section_image_paths = section_image_paths or []
        self._active = False
        self._reconstructed = False

        # Per-KP tracking
        # phase: "pending" | "explained" (illustration+question done) | "mastered"
        self._kp_phases: dict[int, str] = {}
        self._kp_questions: dict[int, str] = {}

        for i, kp in enumerate(knowledge_points):
            if kp.get("mastered"):
                self._kp_phases[i] = "mastered"
            else:
                self._kp_phases[i] = "pending"

        # For pausing/resuming when waiting for user input
        self._user_event = asyncio.Event()
        self._user_message: str | None = None

    @property
    def active(self) -> bool:
        return self._active

    @classmethod
    def reconstruct(
        cls,
        session_id: str,
        section_id: str,
        knowledge_points: list[dict],
        section_title: str,
        current_kp_index: int,
        save_illustration_cb: Optional[Callable[[str, str], Awaitable[None]]] = None,
        save_question_cb: Optional[Callable[[str, str], Awaitable[None]]] = None,
        save_mastery_cb: Optional[Callable[[str], Awaitable[None]]] = None,
        save_state_cb: Optional[Callable[[str, int], Awaitable[None]]] = None,
        section_image_paths: Optional[list[str]] = None,
    ) -> "TeachingAgent":
        """Reconstruct an agent from DB state after server restart."""
        agent = cls(
            session_id=session_id,
            section_id=section_id,
            knowledge_points=knowledge_points,
            section_title=section_title,
            save_illustration_cb=save_illustration_cb,
            save_question_cb=save_question_cb,
            save_mastery_cb=save_mastery_cb,
            save_state_cb=save_state_cb,
            section_image_paths=section_image_paths,
        )
        agent.current_kp_index = current_kp_index
        agent._reconstructed = True

        # Derive richer phases from cached KP fields
        for i, kp in enumerate(knowledge_points):
            if kp.get("mastered"):
                agent._kp_phases[i] = "mastered"
            elif kp.get("illustration") and kp.get("question"):
                # Was explained+checked but not yet answered
                agent._kp_phases[i] = "explained"
                agent._kp_questions[i] = kp["question"]
            else:
                agent._kp_phases[i] = "pending"

        return agent

    def receive_message(self, content: str) -> None:
        self._user_message = content
        self._user_event.set()

    async def _wait_for_user(self) -> str:
        self._user_event.clear()
        self._user_message = None
        await self._user_event.wait()
        msg = self._user_message or ""
        self._user_message = None
        return msg

    def _resolve_kp_image_paths(self, idx: int) -> list[str]:
        """Get local file paths for images associated with a specific KP.

        Falls back to all section images if the KP has no specific associations.
        """
        kp = self.knowledge_points[idx]
        urls = kp.get("image_urls", [])
        if not urls:
            return self._section_image_paths

        paths = []
        for url in urls:
            match = re.match(r'/api/images/([^/]+)/(.+)', url)
            if match:
                book_id, filename = match.group(1), match.group(2)
                path = os.path.join(settings.upload_dir, "images", book_id, filename)
                if os.path.isfile(path):
                    paths.append(path)
        return paths if paths else self._section_image_paths

    async def _stream_ai(self, prompt: str, image_paths: list[str] | None = None) -> AsyncGenerator[dict, None]:
        if image_paths:
            content: str | list[dict] = [{"type": "text", "text": prompt}]
            content.extend(build_image_content_blocks(image_paths[:5]))
        else:
            content = prompt

        collected = []
        async for chunk in chat_completion_stream(
            messages=[{"role": "user", "content": content}],
            max_tokens=2048,
            caller="teaching_agent",
        ):
            collected.append(chunk)
            yield {"event": "token", "data": chunk}

        full_text = "".join(collected)
        yield {"event": "stream_complete", "data": json.dumps({"content": full_text})}

    # --- Per-KP processing ---

    async def _explain_and_check(self, idx: int) -> AsyncGenerator[dict, None]:
        """Run EXPLAIN + CHECK for a single KP. Sets phase to 'explained'."""
        kp = self.knowledge_points[idx]

        # --- EXPLAIN ---
        self.state = "explain"
        yield {"event": "state_change", "data": json.dumps({
            "state": "explain", "current_kp_index": idx,
        })}

        cached_illustration = kp.get("illustration")
        if cached_illustration:
            yield {"event": "token", "data": cached_illustration}
            yield {"event": "stream_complete", "data": json.dumps({"content": cached_illustration})}
        else:
            prompt = EXPLAIN_SYSTEM_PROMPT.format(
                concept=kp["concept"],
                explanation=kp["explanation"],
                difficulty=kp["difficulty"],
                section_title=self.section_title,
            )
            illustration_text = ""
            kp_image_paths = self._resolve_kp_image_paths(idx)
            async for event in self._stream_ai(prompt, image_paths=kp_image_paths):
                if event["event"] == "stream_complete":
                    illustration_text = json.loads(event["data"])["content"]
                yield event

            if illustration_text and self._save_illustration_cb:
                try:
                    await self._save_illustration_cb(kp["id"], illustration_text)
                    kp["illustration"] = illustration_text
                except Exception as e:
                    logger.warning("Failed to cache illustration for KP %s: %s", kp["id"], e)

        # --- CHECK ---
        self.state = "check"
        yield {"event": "state_change", "data": json.dumps({
            "state": "check", "current_kp_index": idx,
        })}

        cached_question = kp.get("question")
        if cached_question:
            self._kp_questions[idx] = cached_question
            yield {"event": "token", "data": cached_question}
            yield {"event": "stream_complete", "data": json.dumps({"content": cached_question})}
        else:
            check_prompt = CHECK_SYSTEM_PROMPT.format(
                concept=kp["concept"],
                explanation=kp["explanation"],
            )
            question_text = ""
            async for event in self._stream_ai(check_prompt):
                if event["event"] == "stream_complete":
                    question_text = json.loads(event["data"])["content"]
                yield event

            self._kp_questions[idx] = question_text
            if question_text and self._save_question_cb:
                try:
                    await self._save_question_cb(kp["id"], question_text)
                    kp["question"] = question_text
                except Exception as e:
                    logger.warning("Failed to cache question for KP %s: %s", kp["id"], e)

        self._kp_phases[idx] = "explained"

    async def _evaluate_answer(self, idx: int, user_answer: str) -> AsyncGenerator[dict, None]:
        """Evaluate user's answer, mark KP as mastered."""
        kp = self.knowledge_points[idx]
        question = self._kp_questions.get(idx, "")

        yield {"event": "user_answer", "data": json.dumps({"content": user_answer})}

        self.state = "evaluate"
        yield {"event": "state_change", "data": json.dumps({
            "state": "evaluate", "current_kp_index": idx,
        })}

        result = await assess_response(
            student_response=user_answer,
            concept=kp["concept"],
            explanation=kp["explanation"],
            question=question,
        )
        yield {"event": "feedback", "data": json.dumps({
            "quality": result.quality,
            "feedback": result.feedback,
        })}

        # Mark as mastered — answering the question = completed
        self._kp_phases[idx] = "mastered"
        if self._save_mastery_cb:
            try:
                await self._save_mastery_cb(kp["id"])
            except Exception as e:
                logger.warning("Failed to save mastery for KP %s: %s", kp["id"], e)

        yield {"event": "kp_complete", "data": json.dumps({"kp_index": idx})}

    def _all_mastered(self) -> bool:
        return all(p == "mastered" for p in self._kp_phases.values())

    def _first_pending(self) -> int | None:
        for i in range(len(self.knowledge_points)):
            if self._kp_phases.get(i, "pending") == "pending":
                return i
        return None

    async def _persist_state(self) -> None:
        """Persist current_kp_index to DB via callback."""
        if self._save_state_cb:
            try:
                await self._save_state_cb(self.session_id, self.current_kp_index)
            except Exception as e:
                logger.warning("Failed to persist state for session %s: %s", self.session_id, e)

    # --- Main event loop ---

    async def _replay_explained_kp(self, idx: int) -> AsyncGenerator[dict, None]:
        """Replay cached illustration + question for a reconstructed KP."""
        kp = self.knowledge_points[idx]

        # Replay illustration
        self.state = "explain"
        yield {"event": "state_change", "data": json.dumps({
            "state": "explain", "current_kp_index": idx,
        })}
        yield {"event": "token", "data": kp["illustration"]}
        yield {"event": "stream_complete", "data": json.dumps({"content": kp["illustration"]})}

        # Replay question
        self.state = "check"
        yield {"event": "state_change", "data": json.dumps({
            "state": "check", "current_kp_index": idx,
        })}
        yield {"event": "token", "data": kp["question"]}
        yield {"event": "stream_complete", "data": json.dumps({"content": kp["question"]})}

    async def event_generator(self) -> AsyncGenerator[dict, None]:
        """Command-driven main loop.

        1. Emit pre-mastered KPs as complete
        2. Auto-start first pending KP (explain+check)
        3. Wait for commands: select:<index> or answer text
        4. Repeat until all KPs mastered or session ends
        """
        self._active = True
        try:
            # Emit pre-mastered KPs
            for i in range(len(self.knowledge_points)):
                if self._kp_phases.get(i) == "mastered":
                    yield {"event": "kp_complete", "data": json.dumps({"kp_index": i})}

            if self._reconstructed:
                # Reconstructed session — resume from persisted state
                phase = self._kp_phases.get(self.current_kp_index, "pending")
                if phase == "explained":
                    # KP was explained+checked, waiting for answer — replay cached content
                    async for event in self._replay_explained_kp(self.current_kp_index):
                        yield event
                elif phase == "mastered":
                    # Current KP already mastered — find next pending
                    first = self._first_pending()
                    if first is None:
                        yield {"event": "done", "data": ""}
                        return
                    self.current_kp_index = first
                    await self._persist_state()
                    async for event in self._explain_and_check(first):
                        yield event
                else:
                    # "pending" — run explain+check from scratch
                    async for event in self._explain_and_check(self.current_kp_index):
                        yield event
            else:
                # Fresh session — find first pending KP and auto-start
                first = self._first_pending()
                if first is None:
                    yield {"event": "done", "data": ""}
                    return

                self.current_kp_index = first
                await self._persist_state()
                async for event in self._explain_and_check(first):
                    yield event

            # Command loop
            while True:
                yield {"event": "waiting", "data": json.dumps({
                    "current_kp_index": self.current_kp_index,
                })}

                user_input = await self._wait_for_user()

                if user_input.startswith("select:"):
                    # User clicked a KP
                    try:
                        target = int(user_input.split(":")[1])
                    except (ValueError, IndexError):
                        continue
                    if not (0 <= target < len(self.knowledge_points)):
                        continue

                    phase = self._kp_phases.get(target, "pending")
                    if phase == "mastered":
                        # Already done — just acknowledge
                        continue

                    self.current_kp_index = target
                    await self._persist_state()

                    if phase == "pending":
                        # Run explain+check for this KP
                        async for event in self._explain_and_check(target):
                            yield event
                    # If "explained", KP already has illustration+question — just wait for answer

                else:
                    # Treat as answer to current KP
                    idx = self.current_kp_index
                    if self._kp_phases.get(idx) != "explained":
                        # Not ready for an answer (pending or already mastered)
                        continue

                    async for event in self._evaluate_answer(idx, user_input):
                        yield event

                    if self._all_mastered():
                        yield {"event": "done", "data": ""}
                        return

        except Exception as e:
            logger.error("Teaching agent error for session %s: %s", self.session_id, e)
            yield {"event": "error", "data": str(e)}
        finally:
            self._active = False
            remove_agent(self.session_id)
