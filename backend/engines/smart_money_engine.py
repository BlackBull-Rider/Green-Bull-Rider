from typing import Dict


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def calculate_smart_money_score(row: Dict) -> Dict:
    score = 0

    breakout_score = row.get("breakout_score", 0) or 0
    swing_score = row.get("swing_score", 0) or 0

    trend = str(row.get("trend", "")).upper()

    volume = row.get("volume", 0) or 0
    volume_avg20 = row.get("volume_avg20", 0) or 0

    # FIX
    cmp_price = row.get("close", 0) or 0

    vwap = row.get("vwap", 0) or 0
    atr = row.get("atr", 0) or 0
    adx = row.get("adx", 0) or 0

    relative_strength = row.get("relative_strength", 0) or 0

    score += min(25, breakout_score)

    score += min(15, swing_score / 2)

    if trend == "BULLISH":
        score += 15
    elif trend == "UPTREND":
        score += 10

    if volume_avg20 > 0:
        ratio = volume / volume_avg20

        if ratio >= 2:
            score += 15
        elif ratio >= 1.5:
            score += 10
        elif ratio >= 1.2:
            score += 5

    if cmp_price > vwap:
        score += 10

    if adx >= 30:
        score += 10
    elif adx >= 25:
        score += 7
    elif adx >= 20:
        score += 4

    if atr > 0:
        score += 5

    if relative_strength >= 80:
        score += 5
    elif relative_strength >= 60:
        score += 3

    score = clamp(score)

    if score >= 85:
        activity = "HEAVY ACCUMULATION"
    elif score >= 70:
        activity = "ACCUMULATION"
    elif score >= 55:
        activity = "NEUTRAL"
    else:
        activity = "DISTRIBUTION"

    return {
        "score": round(score, 2),
        "activity": activity,
    }
