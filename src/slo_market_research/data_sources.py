from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from io import StringIO

import pandas as pd
import requests


@dataclass(frozen=True)
class HistoricalSource:
    """HTTP CSV/JSON source descriptor; no credentials are stored here."""
    name: str
    url: str


def read_ohlcv_csv(url: str) -> pd.DataFrame:
    """Read a public OHLCV CSV and normalize common column names.

    The research project deliberately keeps acquisition separate from scoring.
    Missing/unavailable data is raised rather than replaced with fabricated data.
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    frame = pd.read_csv(StringIO(response.text))
    frame.columns = [str(c).strip().lower().replace(" ", "_") for c in frame.columns]
    required = {"date", "open", "high", "low", "close"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required OHLCV columns: {sorted(missing)}")
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    for col in ["open", "high", "low", "close", "volume"]:
        if col in frame:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")
    return frame.sort_values("date").reset_index(drop=True)


def validate_history(frame: pd.DataFrame, minimum_rows: int = 60) -> None:
    if len(frame) < minimum_rows:
        raise ValueError(f"Only {len(frame)} rows available; need at least {minimum_rows}")
    if frame["date"].duplicated().any():
        raise ValueError("Historical data contains duplicate dates")
    if frame[["open", "high", "low", "close"]].isna().any().any():
        raise ValueError("Historical OHLC data contains missing values")
    if (frame["high"] < frame["low"]).any():
        raise ValueError("Historical data contains high < low")


def date_range(frame: pd.DataFrame) -> tuple[date, date]:
    return frame["date"].iloc[0].date(), frame["date"].iloc[-1].date()
