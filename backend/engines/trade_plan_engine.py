from typing import Dict


def calculate_trade_plan(row: Dict) -> Dict:
    cmp_price = row.get("cmp", 0) or 0
    atr = row.get("atr", 0) or 0
    trend = str(row.get("trend", "")).upper()
    adx = row.get("adx", 0) or 0
    supertrend = row.get("supertrend", 0) or 0

    if cmp_price <= 0:
        return {
            "entry": 0,
            "sl": 0,
            "target1": 0,
            "target2": 0,
            "target3": 0,
            "rr": 0,
            "signal": "INVALID"
        }

    # Entry
    entry = cmp_price

    # Stop Loss
    if supertrend > 0:
        sl = min(supertrend, cmp_price - atr)
    else:
        sl = cmp_price - atr

    risk = entry - sl

    if risk <= 0:
        risk = atr

    # Targets
    target1 = entry + (risk * 2)
    target2 = entry + (risk * 3)
    target3 = entry + (risk * 5)

    rr = round((target3 - entry) / risk, 2)

    # Signal Strength
    if trend in ["BULLISH", "UPTREND"] and adx >= 25:
        signal = "BUY"
    elif trend in ["BULLISH", "UPTREND"]:
        signal = "WATCH"
    else:
        signal = "AVOID"

    return {
        "entry": round(entry, 2),
        "sl": round(sl, 2),
        "target1": round(target1, 2),
        "target2": round(target2, 2),
        "target3": round(target3, 2),
        "rr": rr,
        "signal": signal
    }
