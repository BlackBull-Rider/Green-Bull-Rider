from typing import Dict


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def calculate_swing_score(row: Dict) -> Dict:
    score = 0

    rsi = row.get("rsi", 0) or 0
    macd = row.get("macd", 0) or 0
    macd_signal = row.get("macd_signal", 0) or 0
    adx = row.get("adx", 0) or 0
    plus_di = row.get("plus_di", 0) or 0
    minus_di = row.get("minus_di", 0) or 0

    # FIX
    cmp_price = row.get("close", 0) or 0

    ema20 = row.get("ema20", 0) or 0
    ema50 = row.get("ema50", 0) or 0
    supertrend = row.get("supertrend", 0) or 0

    volume = row.get("volume", 0) or 0
    volume_avg20 = row.get("volume_avg20", 0) or 0

    if 55 <= rsi <= 75:
        score += 15
    elif 50 <= rsi <= 80:
        score += 10
    elif rsi > 45:
        score += 5

    if macd > macd_signal:
        score += 20

    if adx >= 30:
        score += 15
    elif adx >= 25:
        score += 10
    elif adx >= 20:
        score += 5

    if plus_di > minus_di:
        score += 10

    if cmp_price > ema20 > ema50:
        score += 15
    elif cmp_price > ema20:
        score += 8

    if cmp_price > supertrend:
        score += 15

    if volume_avg20 > 0:
        ratio = volume / volume_avg20

        if ratio >= 2:
            score += 10
        elif ratio >= 1.5:
            score += 7
        elif ratio >= 1.2:
            score += 4

    score = clamp(score)

    if score >= 85:
        signal = "BUY"
        strength = "STRONG"
    elif score >= 70:
        signal = "BUY"
        strength = "MODERATE"
    elif score >= 55:
        signal = "WATCH"
        strength = "NEUTRAL"
    else:
        signal = "AVOID"
        strength = "WEAK"

    return {
        "score": round(score, 2),
        "signal": signal,
        "strength": strength,
    }
