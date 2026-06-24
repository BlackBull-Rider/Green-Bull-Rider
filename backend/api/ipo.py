from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.ipo_screener import (
    run_ipo_screener
)

router = APIRouter(
    prefix="/ipo",
    tags=["IPO Hunter"]
)


class IPOFilter(BaseModel):

    min_ipo_score: float = 0
    min_volume_surge: float = 0
    min_institutional: float = 0


@router.get("/")
def get_ipo():

    results = run_ipo_screener()

    return {
        "count": len(results),
        "results": results
    }


@router.post("/search")
def search_ipo(
    filters: IPOFilter
):

    results = run_ipo_screener(
        filters.dict()
    )

    return {
        "count": len(results),
        "results": results
    }
