from backend.database.connection import get_connection
from backend.engines.ai_engine import analyze_stock


def run_ipo_screener(filters=None):

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

        try:

            analysis = analyze_stock(stock)

            ipo_score = calculate_ipo_score(
                stock,
                analysis
            )

            analysis["ipo_score"] = ipo_score

            analysis["listing_discount"] = (
                stock.get(
                    "listing_discount",
                    0
                ) or 0
            )

            analysis["volume_surge"] = (
                stock.get(
                    "volume_ratio",
                    0
                ) or 0
            )

            if ipo_score < filters.get(
                "min_ipo_score",
                0
            ) if filters else False:
                continue

            results.append(analysis)

        except Exception:
            continue

    results.sort(
        key=lambda x: x.get(
            "ipo_score",
            0
        ),
        reverse=True
    )

    return results


def calculate_ipo_score(
    stock,
    analysis
):

    score = 0

    listing_discount = (
        stock.get(
            "listing_discount",
            0
        ) or 0
    )

    institutional = (
        stock.get(
            "institutional_holding",
            0
        ) or 0
    )

    volume_ratio = (
        stock.get(
            "volume_ratio",
            0
        ) or 0
    )

    swing_score = (
        analysis.get(
            "swing_score",
            0
        ) or 0
    )

    if listing_discount > 20:
        score += 25

    elif listing_discount > 10:
        score += 15

    if institutional > 10:
        score += 25

    elif institutional > 5:
        score += 15

    if volume_ratio > 3:
        score += 25

    elif volume_ratio > 2:
        score += 15

    score += (
        swing_score * 0.25
    )

    return round(score, 2)
