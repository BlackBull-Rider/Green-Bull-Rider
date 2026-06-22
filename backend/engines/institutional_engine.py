from typing import Dict


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def calculate_institutional_score(row: Dict) -> Dict:
    score = 0

    promoter = row.get("promoter_holding", 0) or 0
    fii = row.get("fii_holding", 0) or 0
    dii = row.get("dii_holding", 0) or 0
    institutional = row.get("institutional_holding", 0) or 0

    # Promoter Holding (30)
    if promoter >= 70:
        score += 30
    elif promoter >= 60:
        score += 25
    elif promoter >= 50:
        score += 20
    elif promoter >= 40:
        score += 10

    # Institutional Holding (30)
    if institutional >= 50:
        score += 30
    elif institutional >= 40:
        score += 25
    elif institutional >= 30:
        score += 20
    elif institutional >= 20:
        score += 10

    # FII Holding (20)
    if fii >= 20:
        score += 20
    elif fii >= 15:
        score += 15
    elif fii >= 10:
        score += 10
    elif fii >= 5:
        score += 5

    # DII Holding (20)
    if dii >= 20:
        score += 20
    elif dii >= 15:
        score += 15
    elif dii >= 10:
        score += 10
    elif dii >= 5:
        score += 5

    score = clamp(score)

    return {
        "score": round(score, 2)
    }
