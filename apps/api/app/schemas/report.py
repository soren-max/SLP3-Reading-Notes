from pydantic import BaseModel


class ReportRead(BaseModel):
    progress_percent: int
    current_stage: str
    completed_chapters: list[str]
    current_gains: list[str]
    next_plan: list[str]
    research_relation: str
    wechat_text: str
