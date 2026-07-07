from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.report import ReportRead
from app.services.report import build_report

router = APIRouter(prefix="/api/report", tags=["report"])


@router.get("", response_model=ReportRead)
def read_report(db: Session = Depends(get_db)):
    return build_report(db)
