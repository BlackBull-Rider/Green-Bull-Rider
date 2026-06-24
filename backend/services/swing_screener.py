from backend.database.connection import get_connection
from backend.engines.ai_engine import analyze_stock


def run_swing_screener(filters=None):

    conn = get_connection()

    query = """
    SELECT *
    FROM stock_master sm
    LEFT JOIN latest_indicators li
        ON sm.symbol = li.symbol
    LEFT JOIN fundamental_data fd
        ON sm.symbol = fd.symbol
    """

    rows = conn.execute(query).fetchall()

    columns = [
        x[0]
        for x in conn.execute(query).description
    ]

    conn.close()

    results = []

    for row in rows:

        stock = dict(zip(columns, row))

        if not _passes_filter(stock, filters):
            continue

        try:

            analysis = analyze_stock(stock)

            if (
                analysis.get("swing_signal") == "BUY"
                or analysis.get("swing_score", 0) >= 70
            ):
                results.append(analysis)

        except Exception:
            continue

    results.sort(
        key=lambda x: x.get("swing_score", 0),
        reverse=True
    )

    return results


def _passes_filter(stock, filters):

    if not filters:
        return True

    rsi = stock.get("rsi", 0) or 0
    adx = stock.get("adx", 0) or 0
    volume_ratio = stock.get("volume_ratio", 0) or 0

    promoter = stock.get(
        "promoter_holding",
        0
    ) or 0

    institutional = stock.get(
        "institutional_holding",
        0
    ) or 0

    if rsi < filters.get("rsi", 0):
        return False

    if adx < filters.get("adx", 0):
        return False

    if volume_ratio < filters.get(
        "volume_ratio",
        0
    ):
        return False

    if promoter < filters.get(
        "promoter_holding",
        0
    ):
        return False

    if institutional < filters.get(
        "institutional_holding",
        0
    ):
        return False

    return True
