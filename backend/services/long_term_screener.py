from backend.database.connection import get_connection
from backend.engines.ai_engine import analyze_stock


def run_long_term_screener(filters=None):

    conn = get_connection()

    query = """
    SELECT *
    FROM stock_master sm
    LEFT JOIN fundamental_data fd
        ON sm.symbol = fd.symbol
    LEFT JOIN latest_indicators li
        ON sm.symbol = li.symbol
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

        if not _passes_filter(
            stock,
            filters
        ):
            continue

        try:

            analysis = analyze_stock(stock)

            if analysis:
                results.append(analysis)

        except Exception:
            continue

    results.sort(
        key=lambda x: x["master_score"],
        reverse=True
    )

    return results


def _passes_filter(stock, filters):

    if not filters:
        return True

    roe = stock.get("roe", 0) or 0
    roce = stock.get("roce", 0) or 0
    sales_growth = stock.get(
        "sales_growth",
        0
    ) or 0

    profit_growth = stock.get(
        "profit_growth",
        0
    ) or 0

    debt_equity = stock.get(
        "debt_equity",
        999
    ) or 999

    promoter = stock.get(
        "promoter_holding",
        0
    ) or 0

    institutional = stock.get(
        "institutional_holding",
        0
    ) or 0

    market_cap = stock.get(
        "market_cap",
        0
    ) or 0

    if roe < filters.get(
        "roe",
        0
    ):
        return False

    if roce < filters.get(
        "roce",
        0
    ):
        return False

    if sales_growth < filters.get(
        "sales_growth",
        0
    ):
        return False

    if profit_growth < filters.get(
        "profit_growth",
        0
    ):
        return False

    if debt_equity > filters.get(
        "debt_equity",
        999
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

    if market_cap < filters.get(
        "market_cap",
        0
    ):
        return False

    return True
