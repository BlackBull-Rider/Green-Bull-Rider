from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.swing_screener import (
    run_swing_screener
)

router = APIRouter(
    prefix="/swing",
    tags=["Swing Screener"]
)


class SwingFilter(BaseModel):

    rsi: float = 0
    adx: float = 0
    volume_ratio: float = 0

    promoter_holding: float = 0
    institutional_holding: float = 0


@router.get("/")
def get_swing():

    results = run_swing_screener()

    return {
        "count": len(results),
        "results": results
    }


@router.post("/search")
def search_swing(
    filters: SwingFilter
):

    results = run_swing_screener(
        filters.dict()
    )

    return {
        "count": len(results),
        "results": results
    }
