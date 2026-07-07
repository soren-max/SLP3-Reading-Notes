from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chapter import Chapter


def list_chapters(db: Session) -> list[Chapter]:
    priority_order = {"高": 0, "中": 1, "低": 2}
    chapters = db.scalars(select(Chapter)).all()
    return sorted(chapters, key=lambda c: (priority_order.get(c.priority, 9), c.number))


def get_chapter(db: Session, chapter_id: int) -> Chapter | None:
    return db.get(Chapter, chapter_id)


def update_progress(db: Session, chapter_id: int, status: str) -> Chapter | None:
    chapter = get_chapter(db, chapter_id)
    if chapter is None:
        return None
    chapter.status = status
    db.commit()
    db.refresh(chapter)
    return chapter
