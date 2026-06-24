from fastapi import APIRouter

from backend.services.long_term_screener import (
    run_long_term_screener
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard():

    stocks = run_long_term_screener()

    total_stocks = len(stocks)

    long_term_buy = len([
        x for x in stocks
        if x["master_grade"]
        in ["BUY", "STRONG BUY", "ELITE"]
    ])

    swing_buy = len([
        x for x in stocks
        if x["swing_signal"] == "BUY"
    ])

    smart_money = len([
        x for x in stocks
        if x["smart_money_activity"]
        in [
            "ACCUMULATION",
            "HEAVY ACCUMULATION"
        ]
    ])

    top_bullish_stock = None

    if stocks:
        top_bullish_stock = sorted(
            stocks,
            key=lambda x: x["master_score"],
            reverse=True
        )[0]["symbol"]

    top_volume_stock = "N/A"

    try:
        top_volume_stock = sorted(
            stocks,
            key=lambda x: x.get("volume", 0),
            reverse=True
        )[0]["symbol"]
    except:
        pass

    high_52w_count = len([
        x for x in stocks
        if x["master_score"] >= 70
    ])

    market_trend = "BEARISH"

    bullish = len([
        x for x in stocks
        if x["swing_signal"] == "BUY"
    ])

    if total_stocks > 0:

        bullish_pct = (
            bullish / total_stocks
        ) * 100

        if bullish_pct >= 60:
            market_trend = "BULLISH"

        elif bullish_pct >= 40:
            market_trend = "SIDEWAYS"

    return {
        "total_stocks": total_stocks,
        "long_term_buy": long_term_buy,
        "swing_buy": swing_buy,
        "smart_money": smart_money,
        "high_52w_count": high_52w_count,
        "market_trend": market_trend,
        "top_bullish_stock": top_bullish_stock,
        "top_volume_stock": top_volume_stock
    }


@router.get("/long-term")
def top_long_term():

    stocks = run_long_term_screener()

    stocks.sort(
        key=lambda x: x["master_score"],
        reverse=True
    )

    return stocks[:20]


@router.get("/swing")
def top_swing():

    stocks = run_long_term_screener()

    stocks.sort(
        key=lambda x: x["swing_score"],
        reverse=True
    )

    return stocks[:20]


@router.get("/smart-money")
def top_smart_money():

    stocks = run_long_term_screener()

    stocks.sort(
        key=lambda x: x["smart_money_score"],
        reverse=True
    )

    return stocks[:20]


@router.get("/buy-signals")
def buy_signals():

    stocks = run_long_term_screener()

    result = [
        stock
        for stock in stocks
        if stock["signal"] == "BUY"
    ]

    result.sort(
        key=lambda x: x["master_score"],
        reverse=True
    )

    return result[:50]


@router.get("/breakout")
def breakout_radar():

    stocks = run_long_term_screener()

    result = []

    for stock in stocks:

        if (
            stock["swing_signal"] == "BUY"
            and stock["smart_money_score"] >= 55
        ):
            result.append(stock)

    result.sort(
        key=lambda x: (
            x["smart_money_score"]
            + x["swing_score"]
        ),
        reverse=True
    )

    return result[:30]


@router.get("/near-high")
def near_high():

    stocks = run_long_term_screener()

    result = [
        stock
        for stock in stocks
        if stock["master_score"] >= 70
    ]

    result.sort(
        key=lambda x: x["master_score"],
        reverse=True
    )

    return result[:30]
