from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.note import Note
from app.models.source import Source
from app.schemas.note import NoteCreate, NoteUpdate


def list_notes(
    db: Session,
    chapter_id: int | None = None,
    source_id: int | None = None,
    source_type: str | None = None,
    research_direction: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    q: str | None = None,
    tag: str | None = None,
) -> list[Note]:
    stmt = select(Note).order_by(Note.updated_at.desc())
    if chapter_id:
        stmt = stmt.where(Note.chapter_id == chapter_id)
    if source_id:
        stmt = stmt.where(Note.source_id == source_id)
    notes = list(db.scalars(stmt).all())
    if source_type or research_direction or status or priority:
        source_ids = {
            source.id
            for source in db.scalars(select(Source)).all()
            if (not source_type or source.type == source_type)
            and (not research_direction or research_direction.lower() in source.research_direction.lower())
            and (not status or source.status == status)
            and (not priority or source.priority == priority)
        }
        notes = [n for n in notes if n.source_id in source_ids]
    if q:
        needle = q.lower()
        notes = [n for n in notes if needle in n.title.lower() or needle in n.content.lower()]
    if tag:
        notes = [n for n in notes if tag.lower() in n.tags.lower()]
    return notes


def create_note(db: Session, payload: NoteCreate) -> Note:
    data = payload.model_dump()
    note = Note(**data)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(db: Session, note_id: int, payload: NoteUpdate) -> Note | None:
    note = db.get(Note, note_id)
    if note is None:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: int) -> bool:
    note = db.get(Note, note_id)
    if note is None:
        return False
    db.delete(note)
    db.commit()
    return True
