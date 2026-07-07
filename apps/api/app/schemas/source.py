from pydantic import BaseModel


SOURCE_TYPES = {"book", "paper", "course", "project", "report", "misc"}
SOURCE_STATUSES = {"未开始", "进行中", "已完成"}
SOURCE_PRIORITIES = {"高", "中", "低"}


class SourceBase(BaseModel):
    title: str
    type: str
    author_or_origin: str = ""
    research_direction: str
    description: str = ""
    status: str = "未开始"
    priority: str = "中"


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    title: str | None = None
    type: str | None = None
    author_or_origin: str | None = None
    research_direction: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None


class SourceRead(SourceBase):
    id: int

    model_config = {"from_attributes": True}
