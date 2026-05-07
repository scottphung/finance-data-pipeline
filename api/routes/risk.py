from fastapi import APIRouter

router = APIRouter()

@router.get("/risk")
def risk():
    return {"message": "risk module ready"}