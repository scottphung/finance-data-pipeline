from fastapi import APIRouter

router = APIRouter()

@router.get("/backtest")
def backtest():
    return {"message": "backtest module ready"}