from datetime import datetime

from pydantic import BaseModel


class KnowledgePointResponse(BaseModel):
    id: str
    section_id: str
    concept: str
    explanation: str
    difficulty: int
    order_index: int
    mastery_level: float = 0.0

    model_config = {"from_attributes": True}


class SectionResponse(BaseModel):
    id: str
    chapter_id: str
    title: str
    order_index: int
    summary: str | None = None
    knowledge_points: list[KnowledgePointResponse] = []
    progress: float = 0.0

    model_config = {"from_attributes": True}


class ChapterResponse(BaseModel):
    id: str
    book_id: str
    title: str
    order_index: int
    summary: str | None = None
    sections: list[SectionResponse] = []
    progress: float = 0.0

    model_config = {"from_attributes": True}


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    cover_url: str | None = None
    file_type: str
    total_pages: int
    status: str
    progress: float = 0.0
    total_knowledge_points: int = 0
    mastered_knowledge_points: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BookDetailResponse(BookResponse):
    chapters: list[ChapterResponse] = []


class BookListResponse(BaseModel):
    books: list[BookResponse]
