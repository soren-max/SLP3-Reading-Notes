from fastapi import APIRouter

from app.services.roadmap import get_roadmap

router = APIRouter(prefix="/api/roadmap", tags=["roadmap"])


@router.get("")
def read_roadmap():
    return get_roadmap()
