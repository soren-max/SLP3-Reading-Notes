from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(240), index=True)
    type: Mapped[str] = mapped_column(String(20), index=True)
    author_or_origin: Mapped[str] = mapped_column(String(240), default="")
    research_direction: Mapped[str] = mapped_column(String(300), index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="未开始")
    priority: Mapped[str] = mapped_column(String(20), default="中")

    chapters: Mapped[list["Chapter"]] = relationship(back_populates="source", cascade="all, delete-orphan")
    notes: Mapped[list["Note"]] = relationship(back_populates="source", cascade="all, delete-orphan")
