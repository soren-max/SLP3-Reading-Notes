from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


def list_notes(db: Session, chapter_id: int | None = None, q: str | None = None, tag: str | None = None) -> list[Note]:
    stmt = select(Note).order_by(Note.updated_at.desc())
    if chapter_id:
        stmt = stmt.where(Note.chapter_id == chapter_id)
    notes = list(db.scalars(stmt).all())
    if q:
        needle = q.lower()
        notes = [n for n in notes if needle in n.title.lower() or needle in n.content.lower()]
    if tag:
        notes = [n for n in notes if tag.lower() in n.tags.lower()]
    return notes


def create_note(db: Session, payload: NoteCreate) -> Note:
    note = Note(**payload.model_dump())
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
