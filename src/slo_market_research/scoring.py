from __future__ import annotations

import pandas as pd


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add deterministic underlying-level research features.

    Required columns: open, high, low, close, volume.
    """
    out = df.copy()
    out["ret_1d"] = out["close"].pct_change()
    out["ret_5d"] = out["close"].pct_change(5)
    out["ret_20d"] = out["close"].pct_change(20)
    out["ma20"] = out["close"].rolling(20).mean()
    out["ma50"] = out["close"].rolling(50).mean()
    out["trend"] = (out["ma20"] > out["ma50"]).astype(int)
    out["range_pct"] = (out["high"] - out["low"]) / out["close"].replace(0, pd.NA)
    out["volatility_20d"] = out["ret_1d"].rolling(20).std() * (252**0.5)
    out["volume_ratio_20d"] = out["volume"] / out["volume"].rolling(20).mean()
    out["high_20d"] = out["high"].rolling(20).max().shift(1)
    out["low_20d"] = out["low"].rolling(20).min().shift(1)
    out["breakout_20d"] = out["close"] > out["high_20d"]
    out["breakdown_20d"] = out["close"] < out["low_20d"]
    return out


def score_latest(df: pd.DataFrame) -> dict[str, float | str | bool]:
    """Create an ex-ante research score from the latest completed bar."""
    x = add_features(df).iloc[-1]
    bullish = 0.0
    bearish = 0.0
    bullish += 25 if x["trend"] == 1 else 0
    bearish += 25 if x["trend"] == 0 else 0
    bullish += max(min(float(x["ret_5d"] or 0) * 500, 20), 0)
    bearish += max(min(-float(x["ret_5d"] or 0) * 500, 20), 0)
    bullish += 20 if bool(x["breakout_20d"]) else 0
    bearish += 20 if bool(x["breakdown_20d"]) else 0
    volume_bonus = min(max((float(x["volume_ratio_20d"] or 0) - 1) * 20, 0), 15)
    if bullish > bearish:
        bullish += volume_bonus
    elif bearish > bullish:
        bearish += volume_bonus
    signal = "CALL_HYPOTHESIS" if bullish >= 60 and bullish > bearish else "PUT_HYPOTHESIS" if bearish >= 60 and bearish > bullish else "NO_TRADE"
    return {"bullish_score": round(bullish, 2), "bearish_score": round(bearish, 2), "signal": signal}
