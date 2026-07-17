from datetime import date

from pydantic import BaseModel


class InternRecordCreate(BaseModel):
    day: int
    title: str
    content: str
    tags: str = ""


class InternRecordUpdate(BaseModel):
    day: int | None = None
    title: str | None = None
    content: str | None = None
    tags: str | None = None


class InternRecordRead(BaseModel):
    id: int
    day: int
    title: str
    content: str
    tags: str
    record_date: date
    created_at: date

    model_config = {"from_attributes": True}