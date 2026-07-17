from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.intern import InternRecord
from app.schemas.intern import InternRecordCreate, InternRecordUpdate


def list_intern_records(db: Session) -> list[InternRecord]:
    stmt = select(InternRecord).order_by(InternRecord.day.asc())
    return list(db.scalars(stmt).all())


def get_intern_record(db: Session, record_id: int) -> InternRecord | None:
    return db.get(InternRecord, record_id)


def create_intern_record(db: Session, payload: InternRecordCreate) -> InternRecord:
    data = payload.model_dump()
    record = InternRecord(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_intern_record(db: Session, record_id: int, payload: InternRecordUpdate) -> InternRecord | None:
    record = db.get(InternRecord, record_id)
    if record is None:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


def delete_intern_record(db: Session, record_id: int) -> bool:
    record = db.get(InternRecord, record_id)
    if record is None:
        return False
    db.delete(record)
    db.commit()
    return True