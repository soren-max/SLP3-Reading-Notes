from pydantic import BaseModel


class ChapterBase(BaseModel):
    number: int
    title: str
    priority: str
    status: str
    mastery: str
    relevance_score: int
    research_relation: str
    positioning: str
    core_concepts: list[str]
    outline: str
    formulas_algorithms: str
    examples: str
    summary: str
    mentor_questions: list[str]
    research_links: str
    resources: list[str]
    tags: list[str]


class ChapterRead(ChapterBase):
    id: int

    model_config = {"from_attributes": True}


class ChapterListItem(BaseModel):
    id: int
    number: int
    title: str
    priority: str
    status: str
    mastery: str
    relevance_score: int
    research_relation: str
    tags: list[str]

    model_config = {"from_attributes": True}


class ProgressUpdate(BaseModel):
    status: str
