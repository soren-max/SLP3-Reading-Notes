from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.source import SOURCE_PRIORITIES, SOURCE_STATUSES, SOURCE_TYPES, SourceCreate, SourceRead, SourceUpdate
from app.services.sources import create_source, delete_source, get_source, list_sources, update_source

router = APIRouter(prefix="/api/sources", tags=["sources"])


def validate_source_fields(source_type: str | None = None, status: str | None = None, priority: str | None = None) -> None:
    if source_type is not None and source_type not in SOURCE_TYPES:
        raise HTTPException(status_code=422, detail="Invalid source type")
    if status is not None and status not in SOURCE_STATUSES:
        raise HTTPException(status_code=422, detail="Invalid source status")
    if priority is not None and priority not in SOURCE_PRIORITIES:
        raise HTTPException(status_code=422, detail="Invalid source priority")


@router.get("", response_model=list[SourceRead])
def read_sources(
    source_type: str | None = None,
    research_direction: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db),
):
    validate_source_fields(source_type=source_type, status=status, priority=priority)
    return list_sources(db, source_type=source_type, research_direction=research_direction, status=status, priority=priority)


@router.get("/{source_id}", response_model=SourceRead)
def read_source(source_id: int, db: Session = Depends(get_db)):
    source = get_source(db, source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.post("", response_model=SourceRead, status_code=201)
def post_source(payload: SourceCreate, db: Session = Depends(get_db)):
    validate_source_fields(source_type=payload.type, status=payload.status, priority=payload.priority)
    return create_source(db, payload)


@router.patch("/{source_id}", response_model=SourceRead)
def patch_source(source_id: int, payload: SourceUpdate, db: Session = Depends(get_db)):
    validate_source_fields(source_type=payload.type, status=payload.status, priority=payload.priority)
    source = update_source(db, source_id, payload)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.delete("/{source_id}", status_code=204)
def remove_source(source_id: int, db: Session = Depends(get_db)):
    if not delete_source(db, source_id):
        raise HTTPException(status_code=404, detail="Source not found")
    return Response(status_code=204)
