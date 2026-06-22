from backend.engines.compounder_engine import calculate_compounder_score
from backend.engines.swing_engine import calculate_swing_score
from backend.engines.smart_money_engine import calculate_smart_money_score
from backend.engines.institutional_engine import calculate_institutional_score
from backend.engines.master_engine import calculate_master_score
from backend.engines.trade_plan_engine import calculate_trade_plan


def analyze_stock(row):

    compounder = calculate_compounder_score(row)

    swing = calculate_swing_score(row)

    smart_money = calculate_smart_money_score(row)

    institutional = calculate_institutional_score(row)

    master = calculate_master_score(
        compounder_score=compounder["score"],
        swing_score=swing["score"],
        smart_money_score=smart_money["score"],
        institutional_score=institutional["score"]
    )

    trade_plan = calculate_trade_plan(row)

    return {
        "symbol": row.get("symbol"),

        "compounder_score": compounder["score"],
        "compounder_grade": compounder["grade"],

        "swing_score": swing["score"],
        "swing_signal": swing["signal"],

        "smart_money_score": smart_money["score"],
        "smart_money_activity": smart_money["activity"],

        "institutional_score": institutional["score"],

        "master_score": master["score"],
        "master_grade": master["grade"],

        "entry": trade_plan["entry"],
        "sl": trade_plan["sl"],
        "target1": trade_plan["target1"],
        "target2": trade_plan["target2"],
        "target3": trade_plan["target3"],
        "rr": trade_plan["rr"],

        "signal": trade_plan["signal"]
    }
