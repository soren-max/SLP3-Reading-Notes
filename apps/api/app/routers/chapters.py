from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chapter import ChapterListItem, ChapterRead, ProgressUpdate
from app.services.chapters import get_chapter, list_chapters, update_progress

router = APIRouter(prefix="/api/chapters", tags=["chapters"])


@router.get("", response_model=list[ChapterListItem])
def read_chapters(db: Session = Depends(get_db)):
    return list_chapters(db)


@router.get("/{chapter_id}", response_model=ChapterRead)
def read_chapter(chapter_id: int, db: Session = Depends(get_db)):
    chapter = get_chapter(db, chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


@router.patch("/{chapter_id}/progress", response_model=ChapterRead)
def patch_progress(chapter_id: int, payload: ProgressUpdate, db: Session = Depends(get_db)):
    if payload.status not in {"未开始", "阅读中", "已完成"}:
        raise HTTPException(status_code=422, detail="Invalid status")
    chapter = update_progress(db, chapter_id, payload.status)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter
