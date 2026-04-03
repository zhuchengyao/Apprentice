from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    book_id: str
    section_id: str


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    mode: str
    timestamp: str


class KnowledgePointBrief(BaseModel):
    id: str
    concept: str
    explanation: str
    difficulty: int
    mastered: bool = False
    illustration: str = ""
    question: str = ""
    image_urls: list[str] = []


class StudySessionResponse(BaseModel):
    id: str
    book_id: str
    section_id: str
    current_kp_index: int
    state: str
    messages: list[MessageResponse] = []
    knowledge_points: list[KnowledgePointBrief] = []


class UserMessageRequest(BaseModel):
    content: str
