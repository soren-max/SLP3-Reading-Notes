from datetime import date

from sqlalchemy import Date, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InternRecord(Base):
    __tablename__ = "intern_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    day: Mapped[int] = mapped_column(Integer, comment="实习第几天")
    title: Mapped[str] = mapped_column(String(300), comment="当日标题")
    content: Mapped[str] = mapped_column(Text, comment="当日内容 Markdown")
    tags: Mapped[str] = mapped_column(String(300), default="", comment="标签，逗号分隔")
    record_date: Mapped[date] = mapped_column(Date, server_default=func.current_date(), comment="记录日期")
    created_at: Mapped[date] = mapped_column(Date, server_default=func.current_date())