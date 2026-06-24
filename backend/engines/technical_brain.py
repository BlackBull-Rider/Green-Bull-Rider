from typing import Dict, List
from math import fabs


TECHNICAL_WEIGHTS = {

    "EMA_ALIGNMENT": 20,
    "PRICE_ABOVE_EMA20": 4,
    "PRICE_ABOVE_EMA50": 6,
    "PRICE_ABOVE_EMA200": 10,

    "RSI_STRONG": 10,
    "RSI_HEALTHY": 6,

    "ADX_STRONG": 10,
    "ADX_MODERATE": 6,

    "MACD_BULLISH": 8,

    "SUPERTREND": 10,

    "VWAP": 5,

    "HIGH_VOLUME": 10,
    "MEDIUM_VOLUME": 5,

    "BREAKOUT": 10
}


class TechnicalBrain:

    @staticmethod
    def _safe(value):

        if value is None:
            return 0

        return float(value)

    @staticmethod
    def _ema_analysis(row):

        score = 0

        reasons = []

        close = TechnicalBrain._safe(
            row.get("close")
        )

        ema20 = TechnicalBrain._safe(
            row.get("ema20")
        )

        ema50 = TechnicalBrain._safe(
            row.get("ema50")
        )

        ema200 = TechnicalBrain._safe(
            row.get("ema200")
        )

        trend = "BEARISH"

        if ema20 > ema50 > ema200:

            score += TECHNICAL_WEIGHTS["EMA_ALIGNMENT"]

            reasons.append(
                "Perfect EMA Alignment"
            )

            trend = "STRONG BULLISH"

        elif ema20 > ema50:

            score += 10

            reasons.append(
                "Bullish EMA Structure"
            )

            trend = "BULLISH"

        if close > ema20:

            score += TECHNICAL_WEIGHTS[
                "PRICE_ABOVE_EMA20"
            ]

        if close > ema50:

            score += TECHNICAL_WEIGHTS[
                "PRICE_ABOVE_EMA50"
            ]

        if close > ema200:

            score += TECHNICAL_WEIGHTS[
                "PRICE_ABOVE_EMA200"
            ]

        return {

            "score": score,

            "trend": trend,

            "reasons": reasons
        }

    @staticmethod
    def _rsi_analysis(row):

        score = 0

        reasons = []

        rsi = TechnicalBrain._safe(
            row.get("rsi")
        )

        state = "WEAK"

        if rsi >= 70:

            score += TECHNICAL_WEIGHTS[
                "RSI_STRONG"
            ]

            state = "VERY STRONG"

            reasons.append(
                "RSI Above 70"
            )

        elif rsi >= 60:

            score += TECHNICAL_WEIGHTS[
                "RSI_HEALTHY"
            ]

            state = "STRONG"

            reasons.append(
                "Healthy RSI"
            )

        elif rsi >= 50:

            score += 3

            state = "POSITIVE"

        elif rsi < 40:

            score -= 8

            state = "WEAK"

        return {

            "score": score,

            "state": state,

            "value": round(
                rsi,
                2
            ),

            "reasons": reasons
        }

    @staticmethod
    def _adx_analysis(row):

        score = 0

        reasons = []

        adx = TechnicalBrain._safe(
            row.get("adx")
        )

        plus_di = TechnicalBrain._safe(
            row.get("plus_di")
        )

        minus_di = TechnicalBrain._safe(
            row.get("minus_di")
        )

        strength = "LOW"

        if adx >= 35:

            score += TECHNICAL_WEIGHTS[
                "ADX_STRONG"
            ]

            strength = "VERY STRONG"

            reasons.append(
                "Strong Trend"
            )

        elif adx >= 25:

            score += TECHNICAL_WEIGHTS[
                "ADX_MODERATE"
            ]

            strength = "STRONG"

        elif adx >= 20:

            score += 3

            strength = "MODERATE"

        if plus_di > minus_di:

            score += 3

            reasons.append(
                "Buyers Dominating"
            )

        return {

            "score": score,

            "strength": strength,

            "value": round(
                adx,
                2
            ),

            "reasons": reasons
        }

@staticmethod
    def _macd_analysis(row):

        score = 0

        reasons = []

        macd = TechnicalBrain._safe(
            row.get("macd")
        )

        signal = TechnicalBrain._safe(
            row.get("macd_signal")
        )

        hist = TechnicalBrain._safe(
            row.get("macd_hist")
        )

        state = "BEARISH"

        if macd > signal:

            score += TECHNICAL_WEIGHTS[
                "MACD_BULLISH"
            ]

            state = "BULLISH"

            reasons.append(
                "MACD Bullish Crossover"
            )

            if hist > 0:

                score += 2

                reasons.append(
                    "Positive Histogram"
                )

        else:

            score -= 4

        return {

            "score": score,

            "state": state,

            "histogram": round(
                hist,
                2
            ),

            "reasons": reasons
        }

    @staticmethod
    def _supertrend_analysis(row):

        score = 0

        reasons = []

        close = TechnicalBrain._safe(
            row.get("close")
        )

        supertrend = TechnicalBrain._safe(
            row.get("supertrend")
        )

        state = "SELL"

        if close > supertrend:

            score += TECHNICAL_WEIGHTS[
                "SUPERTREND"
            ]

            state = "BUY"

            reasons.append(
                "Above Supertrend"
            )

        else:

            score -= 8

        return {

            "score": score,

            "signal": state,

            "reasons": reasons
        }

    @staticmethod
    def _volume_analysis(row):

        score = 0

        reasons = []

        volume = TechnicalBrain._safe(
            row.get("volume")
        )

        avg = TechnicalBrain._safe(
            row.get("volume_avg20")
        )

        ratio = 0

        if avg > 0:

            ratio = volume / avg

        strength = "LOW"

        if ratio >= 2:

            score += TECHNICAL_WEIGHTS[
                "HIGH_VOLUME"
            ]

            strength = "VERY HIGH"

            reasons.append(
                "Volume Explosion"
            )

        elif ratio >= 1.5:

            score += TECHNICAL_WEIGHTS[
                "MEDIUM_VOLUME"
            ]

            strength = "HIGH"

            reasons.append(
                "Strong Volume"
            )

        elif ratio >= 1:

            strength = "NORMAL"

        else:

            strength = "LOW"

        return {

            "score": score,

            "ratio": round(
                ratio,
                2
            ),

            "strength": strength,

            "reasons": reasons
        }

    @staticmethod
    def _vwap_analysis(row):

        score = 0

        reasons = []

        close = TechnicalBrain._safe(
            row.get("close")
        )

        vwap = TechnicalBrain._safe(
            row.get("vwap")
        )

        signal = "BELOW"

        if close > vwap:

            score += TECHNICAL_WEIGHTS[
                "VWAP"
            ]

            signal = "ABOVE"

            reasons.append(
                "Trading Above VWAP"
            )

        return {

            "score": score,

            "signal": signal,

            "reasons": reasons
        }

    @staticmethod
    def _breakout_analysis(row):

        score = 0

        reasons = []

        breakout = TechnicalBrain._safe(
            row.get("breakout_score")
        )

        signal = "NO"

        if breakout >= 80:

            score += 10

            signal = "STRONG"

            reasons.append(
                "Strong Breakout"
            )

        elif breakout >= 60:

            score += 6

            signal = "MODERATE"

            reasons.append(
                "Possible Breakout"
            )

        return {

            "score": score,

            "signal": signal,

            "breakout_score": breakout,

            "reasons": reasons
        }

@staticmethod
    def _support_resistance_analysis(row):

        score = 0

        reasons = []

        close = TechnicalBrain._safe(
            row.get("close")
        )

        r1 = TechnicalBrain._safe(
            row.get("r1")
        )

        r2 = TechnicalBrain._safe(
            row.get("r2")
        )

        s1 = TechnicalBrain._safe(
            row.get("s1")
        )

        s2 = TechnicalBrain._safe(
            row.get("s2")
        )

        signal = "NEUTRAL"

        resistance_distance = 0

        support_distance = 0

        if r1 > 0:

            resistance_distance = (
                (r1 - close) / close
            ) * 100

        if s1 > 0:

            support_distance = (
                (close - s1) / close
            ) * 100

        if close > r1 and r1 > 0:

            score += 10

            signal = "RESISTANCE BREAKOUT"

            reasons.append(
                "Price Above R1"
            )

        elif resistance_distance <= 2:

            score += 5

            reasons.append(
                "Near Resistance"
            )

        if support_distance <= 2:

            score += 4

            reasons.append(
                "Support Holding"
            )

        return {

            "score": score,

            "signal": signal,

            "resistance_distance":
                round(resistance_distance,2),

            "support_distance":
                round(support_distance,2),

            "reasons": reasons
        }


    @staticmethod
    def _volatility_analysis(row):

        score = 0

        reasons = []

        atr = TechnicalBrain._safe(
            row.get("atr")
        )

        close = TechnicalBrain._safe(
            row.get("close")
        )

        volatility = 0

        if close > 0:

            volatility = (
                atr / close
            ) * 100

        state = "NORMAL"

        if volatility < 2:

            score += 6

            state = "LOW"

            reasons.append(
                "Controlled Volatility"
            )

        elif volatility < 4:

            score += 3

            state = "MEDIUM"

        else:

            score -= 3

            state = "HIGH"

            reasons.append(
                "High Volatility"
            )

        return {

            "score": score,

            "volatility":
                round(volatility,2),

            "state": state,

            "reasons": reasons
        }


    @staticmethod
    def _momentum_analysis(row):

        score = 0

        reasons = []

        rsi = TechnicalBrain._safe(
            row.get("rsi")
        )

        adx = TechnicalBrain._safe(
            row.get("adx")
        )

        macd = TechnicalBrain._safe(
            row.get("macd")
        )

        signal = TechnicalBrain._safe(
            row.get("macd_signal")
        )

        state = "WEAK"

        if (
            rsi >= 60
            and adx >= 25
            and macd > signal
        ):

            score += 15

            state = "STRONG"

            reasons.append(
                "Momentum Confirmed"
            )

        elif (
            rsi >= 50
        ):

            score += 8

            state = "MODERATE"

        return {

            "score": score,

            "state": state,

            "reasons": reasons
        }


    @staticmethod
    def _confidence_analysis(total):

        if total >= 90:

            return 98

        if total >= 80:

            return 92

        if total >= 70:

            return 85

        if total >= 60:

            return 75

        if total >= 50:

            return 65

        return 40

@staticmethod
    def analyze(row):

        ema = TechnicalBrain._ema_analysis(row)

        rsi = TechnicalBrain._rsi_analysis(row)

        adx = TechnicalBrain._adx_analysis(row)

        macd = TechnicalBrain._macd_analysis(row)

        supertrend = TechnicalBrain._supertrend_analysis(row)

        volume = TechnicalBrain._volume_analysis(row)

        vwap = TechnicalBrain._vwap_analysis(row)

        breakout = TechnicalBrain._breakout_analysis(row)

        support = TechnicalBrain._support_resistance_analysis(row)

        volatility = TechnicalBrain._volatility_analysis(row)

        momentum = TechnicalBrain._momentum_analysis(row)

        total = (

            ema["score"]

            + rsi["score"]

            + adx["score"]

            + macd["score"]

            + supertrend["score"]

            + volume["score"]

            + vwap["score"]

            + breakout["score"]

            + support["score"]

            + volatility["score"]

            + momentum["score"]

        )

        total = max(
            0,
            min(
                100,
                round(total, 2)
            )
        )

        confidence = TechnicalBrain._confidence_analysis(
            total
        )

        signal = "SELL"

        allocation = 0

        risk = "HIGH"

        if total >= 85:

            signal = "STRONG BUY"

            allocation = 20

            risk = "LOW"

        elif total >= 75:

            signal = "BUY"

            allocation = 15

            risk = "LOW"

        elif total >= 60:

            signal = "ACCUMULATE"

            allocation = 10

            risk = "MEDIUM"

        elif total >= 45:

            signal = "HOLD"

            allocation = 0

            risk = "MEDIUM"

        reasons = []

        for item in [

            ema,

            rsi,

            adx,

            macd,

            supertrend,

            volume,

            vwap,

            breakout,

            support,

            volatility,

            momentum

        ]:

            reasons.extend(
                item["reasons"]
            )

        reasons = list(
            dict.fromkeys(
                reasons
            )
        )

        return {

            "technical_score": total,

            "technical_signal": signal,

            "confidence": confidence,

            "allocation": allocation,

            "risk": risk,

            "trend": ema["trend"],

            "momentum": momentum["state"],

            "volume_strength":
                volume["strength"],

            "volume_ratio":
                volume["ratio"],

            "breakout":
                breakout["signal"],

            "breakout_score":
                breakout["breakout_score"],

            "support_signal":
                support["signal"],

            "support_distance":
                support["support_distance"],

            "resistance_distance":
                support["resistance_distance"],

            "volatility":
                volatility["volatility"],

            "volatility_state":
                volatility["state"],

            "reasons": reasons

        }
