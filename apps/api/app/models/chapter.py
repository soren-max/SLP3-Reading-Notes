from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(180), index=True)
    priority: Mapped[str] = mapped_column(String(20), index=True)
    status: Mapped[str] = mapped_column(String(20), default="未开始")
    mastery: Mapped[str] = mapped_column(String(20), default="理解")
    relevance_score: Mapped[int] = mapped_column(Integer, default=50)
    research_relation: Mapped[str] = mapped_column(Text)
    positioning: Mapped[str] = mapped_column(Text)
    core_concepts: Mapped[list[str]] = mapped_column(JSON, default=list)
    outline: Mapped[str] = mapped_column(Text, default="")
    formulas_algorithms: Mapped[str] = mapped_column(Text, default="")
    examples: Mapped[str] = mapped_column(Text, default="")
    summary: Mapped[str] = mapped_column(Text, default="")
    mentor_questions: Mapped[list[str]] = mapped_column(JSON, default=list)
    research_links: Mapped[str] = mapped_column(Text, default="")
    resources: Mapped[list[str]] = mapped_column(JSON, default=list)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)

    notes: Mapped[list["Note"]] = relationship(back_populates="chapter", cascade="all, delete-orphan")
