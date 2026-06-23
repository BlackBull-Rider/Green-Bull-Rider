from typing import Dict


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def calculate_compounder_score(row: Dict) -> Dict:

    score = 0

    # Yahoo returns ROE/ROCE in decimal form
    roe = (row.get("roe", 0) or 0) * 100
    roce = (row.get("roce", 0) or 0) * 100

    sales_growth = row.get("sales_growth")
    profit_growth = row.get("profit_growth")

    debt_equity = row.get("debt_equity")
    institutional_holding = row.get("institutional_holding")
    free_cash_flow = row.get("free_cash_flow")

    market_cap = row.get("market_cap")
    promoter_holding = row.get("promoter_holding")

    # Handle NULL values
    if sales_growth is None:
        sales_growth = 10

    if profit_growth is None:
        profit_growth = 10

    if debt_equity is None:
        debt_equity = 1

    if institutional_holding is None:
        institutional_holding = 0

    if promoter_holding is None:
        promoter_holding = 0

    if free_cash_flow is None:
        free_cash_flow = 0

    # -------------------------
    # ROE (15)
    # -------------------------
    if roe >= 25:
        score += 15
    elif roe >= 20:
        score += 12
    elif roe >= 15:
        score += 8
    elif roe >= 10:
        score += 4

    # -------------------------
    # ROCE (15)
    # -------------------------
    if roce >= 25:
        score += 15
    elif roce >= 20:
        score += 12
    elif roce >= 15:
        score += 8
    elif roce >= 10:
        score += 4

    # -------------------------
    # Sales Growth (15)
    # -------------------------
    if sales_growth >= 20:
        score += 15
    elif sales_growth >= 15:
        score += 12
    elif sales_growth >= 10:
        score += 8
    elif sales_growth >= 5:
        score += 4

    # -------------------------
    # Profit Growth (15)
    # -------------------------
    if profit_growth >= 20:
        score += 15
    elif profit_growth >= 15:
        score += 12
    elif profit_growth >= 10:
        score += 8
    elif profit_growth >= 5:
        score += 4

    # -------------------------
    # Debt Equity (15)
    # -------------------------
    if debt_equity <= 0.3:
        score += 15
    elif debt_equity <= 0.5:
        score += 12
    elif debt_equity <= 1:
        score += 8
    elif debt_equity <= 2:
        score += 4

    # -------------------------
    # Institutional Holding (10)
    # -------------------------
    if institutional_holding >= 40:
        score += 10
    elif institutional_holding >= 25:
        score += 7
    elif institutional_holding >= 10:
        score += 4

    # -------------------------
    # Promoter Holding (5)
    # -------------------------
    if promoter_holding >= 70:
        score += 5
    elif promoter_holding >= 50:
        score += 3
    elif promoter_holding >= 25:
        score += 1

    # -------------------------
    # Free Cash Flow (15)
    # -------------------------
    if free_cash_flow > 0:
        score += 15

    # -------------------------
    # Market Cap Bonus (5)
    # -------------------------
    if market_cap:
        if market_cap >= 100000000000:
            score += 5
        elif market_cap >= 10000000000:
            score += 3

    score = clamp(score)

    if score >= 85:
        grade = "A+ Compounder"
    elif score >= 70:
        grade = "A Compounder"
    elif score >= 55:
        grade = "B Compounder"
    elif score >= 40:
        grade = "Watchlist"
    else:
        grade = "Avoid"

    return {
        "score": round(score, 2),
        "grade": grade
    }
