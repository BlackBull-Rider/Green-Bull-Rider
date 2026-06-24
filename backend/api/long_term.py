from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.long_term_screener import (
    run_long_term_screener
)

router = APIRouter(
    prefix="/long-term",
    tags=["Long Term Screener"]
)


class LongTermFilter(BaseModel):

    roe: Optional[float] = 0
    roce: Optional[float] = 0

    sales_growth: Optional[float] = 0
    profit_growth: Optional[float] = 0

    debt_equity: Optional[float] = 999

    promoter_holding: Optional[float] = 0
    institutional_holding: Optional[float] = 0

    market_cap: Optional[float] = 0


@router.get("/")
def get_long_term():

    results = run_long_term_screener()

    return {
        "count": len(results),
        "results": results[:100]
    }


@router.post("/search")
def search_long_term(
    filters: LongTermFilter
):

    results = run_long_term_screener(
        filters.dict()
    )

    return {
        "count": len(results),
        "results": results[:100]
    }
