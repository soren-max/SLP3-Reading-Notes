from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.note import NoteCreate, NoteRead, NoteUpdate
from app.services.notes import create_note, delete_note, list_notes, update_note

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.get("", response_model=list[NoteRead])
def read_notes(chapter_id: int | None = None, q: str | None = None, tag: str | None = None, db: Session = Depends(get_db)):
    return list_notes(db, chapter_id=chapter_id, q=q, tag=tag)


@router.post("", response_model=NoteRead, status_code=201)
def post_note(payload: NoteCreate, db: Session = Depends(get_db)):
    return create_note(db, payload)


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)):
    note = update_note(db, note_id, payload)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", status_code=204)
def remove_note(note_id: int, db: Session = Depends(get_db)):
    if not delete_note(db, note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    return Response(status_code=204)
