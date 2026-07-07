from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate


def list_sources(
    db: Session,
    source_type: str | None = None,
    research_direction: str | None = None,
    status: str | None = None,
    priority: str | None = None,
) -> list[Source]:
    stmt = select(Source).order_by(Source.priority.asc(), Source.id.asc())
    sources = list(db.scalars(stmt).all())
    if source_type:
        sources = [source for source in sources if source.type == source_type]
    if research_direction:
        needle = research_direction.lower()
        sources = [source for source in sources if needle in source.research_direction.lower()]
    if status:
        sources = [source for source in sources if source.status == status]
    if priority:
        sources = [source for source in sources if source.priority == priority]
    return sources


def get_source(db: Session, source_id: int) -> Source | None:
    return db.get(Source, source_id)


def create_source(db: Session, payload: SourceCreate) -> Source:
    source = Source(**payload.model_dump())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def update_source(db: Session, source_id: int, payload: SourceUpdate) -> Source | None:
    source = get_source(db, source_id)
    if source is None:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(source, key, value)
    db.commit()
    db.refresh(source)
    return source


def delete_source(db: Session, source_id: int) -> bool:
    source = get_source(db, source_id)
    if source is None:
        return False
    db.delete(source)
    db.commit()
    return True
