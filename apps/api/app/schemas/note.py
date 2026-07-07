from datetime import datetime

from pydantic import BaseModel


class NoteCreate(BaseModel):
    source_id: int
    chapter_id: int | None = None
    title: str
    content: str
    tags: str = ""


class NoteUpdate(BaseModel):
    chapter_id: int | None = None
    title: str | None = None
    content: str | None = None
    tags: str | None = None


class NoteRead(BaseModel):
    id: int
    source_id: int
    chapter_id: int | None
    title: str
    content: str
    tags: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
