# SLO Market Research

Independent research project. **This repository is separate from `slo-options` and must not modify or share strategy state with it.**

## Objective

Study historical movement across:
- NIFTY 50
- BANKNIFTY
- The current NSE F&O equity universe

The research produces ranked bullish, bearish and neutral candidates and evaluates whether an underlying historically exhibited conditions that could support a long CALL or long PUT hypothesis.

## Anti-hindsight rule

Signals must use only information available at the signal timestamp. End-of-day results are reported separately from the ex-ante signal. No candidate may be selected merely because it subsequently moved in the expected direction.

## Research layers

1. Universe snapshot
2. Daily OHLCV ingestion
3. Trend and momentum features
4. Volatility and range features
5. Volume/relative-volume features
6. Breakout/breakdown features
7. Cross-sectional ranking
8. CALL/PUT hypothesis score
9. Historical forward-return study
10. Report generation

## Current 19-Aug-2026 market context

NIFTY 50 closed at 24,078.30, down 0.32%, extending its decline to seven consecutive sessions. This context is recorded as an observed market outcome, not as a hindsight signal.

## Data policy

The project must use reproducible historical data sources. Do not fabricate option prices or intraday values. Until a licensed/reliable historical F&O dataset is configured, reports should clearly distinguish available equity/index observations from unavailable option-contract observations.

## Planned reports

- `reports/daily/YYYY-MM-DD.md`
- `reports/rankings/YYYY-MM-DD.csv`
- `reports/forward-study/*.csv`

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

This project is research-only and does not place orders.
