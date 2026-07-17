from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.intern import InternRecordCreate, InternRecordRead, InternRecordUpdate
from app.services.interns import (
    create_intern_record,
    delete_intern_record,
    get_intern_record,
    list_intern_records,
    update_intern_record,
)

router = APIRouter(prefix="/api/interns", tags=["interns"])


@router.get("", response_model=list[InternRecordRead])
def read_intern_records(db: Session = Depends(get_db)):
    return list_intern_records(db)


@router.get("/{record_id}", response_model=InternRecordRead)
def read_intern_record(record_id: int, db: Session = Depends(get_db)):
    record = get_intern_record(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Intern record not found")
    return record


@router.post("", response_model=InternRecordRead, status_code=201)
def post_intern_record(payload: InternRecordCreate, db: Session = Depends(get_db)):
    return create_intern_record(db, payload)


@router.patch("/{record_id}", response_model=InternRecordRead)
def patch_intern_record(record_id: int, payload: InternRecordUpdate, db: Session = Depends(get_db)):
    record = update_intern_record(db, record_id, payload)
    if record is None:
        raise HTTPException(status_code=404, detail="Intern record not found")
    return record


@router.delete("/{record_id}", status_code=204)
def remove_intern_record(record_id: int, db: Session = Depends(get_db)):
    if not delete_intern_record(db, record_id):
        raise HTTPException(status_code=404, detail="Intern record not found")
    return Response(status_code=204)