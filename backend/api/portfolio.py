from fastapi import APIRouter
from fastapi import Depends

from pydantic import BaseModel

from backend.security import (
    get_current_user
)

from backend.services.portfolio_service import (
    buy_stock,
    sell_stock,
    get_holdings,
    get_transactions
)

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)


class TradeRequest(BaseModel):

    symbol: str
    qty: float
    price: float


@router.post("/buy")
def buy(
    request: TradeRequest,
    user=Depends(get_current_user)
):

    return buy_stock(
        user["user_id"],
        request.symbol,
        request.qty,
        request.price
    )


@router.post("/sell")
def sell(
    request: TradeRequest,
    user=Depends(get_current_user)
):

    return sell_stock(
        user["user_id"],
        request.symbol,
        request.qty,
        request.price
    )


@router.get("/holdings")
def holdings(
    user=Depends(get_current_user)
):

    return get_holdings(
        user["user_id"]
    )


@router.get("/transactions")
def transactions(
    user=Depends(get_current_user)
):

    return get_transactions(
        user["user_id"]
    )
