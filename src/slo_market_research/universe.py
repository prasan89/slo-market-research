from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Instrument:
    symbol: str
    category: str


def build_universe(fno_symbols: Iterable[str]) -> list[Instrument]:
    """Build the research universe from an externally supplied current F&O list."""
    instruments = [Instrument("NIFTY", "index"), Instrument("BANKNIFTY", "index")]
    instruments.extend(Instrument(symbol=s, category="stock_fno") for s in sorted(set(fno_symbols)))
    return instruments
