from fastapi import APIRouter, Depends

from backend.security import get_current_user
from backend.user_database.connection import get_user_connection
from backend.database.connection import get_connection

router = APIRouter(
    prefix="/portfolio-analysis",
    tags=["Portfolio Analysis"]
)


@router.get("/")
def portfolio_analysis(
    user=Depends(get_current_user)
):

    user_conn = get_user_connection()
    market_conn = get_connection()

    holdings = user_conn.execute(
        """
        SELECT *
        FROM portfolios
        WHERE user_id=?
        """,
        (user["user_id"],)
    ).fetchall()

    result = []

    invested = 0
    current = 0

    for row in holdings:

        symbol = row["symbol"]
        qty = row["qty"]
        avg_price = row["avg_price"]

        market = market_conn.execute(
            """
            SELECT
                close,
                rsi,
                swing_score,
                breakout_score,
                trend
            FROM latest_indicators
            WHERE symbol=?
            """,
            (symbol,)
        ).fetchone()

        if not market:
            continue

        cmp_price = market["close"]

        invested_value = qty * avg_price
        current_value = qty * cmp_price

        pnl = current_value - invested_value

        invested += invested_value
        current += current_value

        result.append({
            "symbol": symbol,
            "qty": qty,
            "avg_price": avg_price,
            "cmp": cmp_price,
            "invested": round(invested_value,2),
            "current": round(current_value,2),
            "pnl": round(pnl,2),
            "pnl_percent": round(
                (pnl/invested_value)*100,
                2
            ),
            "rsi": market["rsi"],
            "swing_score": market["swing_score"],
            "breakout_score": market["breakout_score"],
            "trend": market["trend"]
        })

    user_conn.close()
    market_conn.close()

    total_pnl = current - invested

    return {
        "total_stocks": len(result),
        "invested_value": round(invested,2),
        "current_value": round(current,2),
        "total_pnl": round(total_pnl,2),
        "total_pnl_percent":
            round(
                (total_pnl/invested)*100,
                2
            ) if invested else 0,
        "holdings": result
    }
