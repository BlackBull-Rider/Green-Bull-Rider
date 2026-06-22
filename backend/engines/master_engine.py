from typing import Dict


def get_grade(score: float) -> str:
    if score >= 90:
        return "ELITE"
    elif score >= 80:
        return "STRONG BUY"
    elif score >= 70:
        return "BUY"
    elif score >= 60:
        return "WATCHLIST"
    return "AVOID"


def calculate_master_score(
    compounder_score: float,
    swing_score: float,
    smart_money_score: float,
    institutional_score: float
) -> Dict:

    master_score = (
        compounder_score * 0.35 +
        swing_score * 0.25 +
        smart_money_score * 0.25 +
        institutional_score * 0.15
    )

    return {
        "score": round(master_score, 2),
        "grade": get_grade(master_score)
    }
