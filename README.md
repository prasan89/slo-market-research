# SLO Market Research

Separate research project from `slo-options`.

## Goal
Study the historical behavior of the NIFTY 50, BANKNIFTY, and the current NSE F&O stock universe to identify repeatable bullish/bearish underlying patterns that could make long CALL/PUT option buying attractive.

This project does **not** modify or share strategy state with `slo-options`.

## Research outputs
- Daily/weekly underlying ranking
- Momentum and trend statistics
- Volatility and drawdown statistics
- Volume/relative-volume statistics
- Breakout/breakdown observations
- CALL/PUT candidate watchlists
- Historical event studies
- Out-of-sample validation

## Anti-hindsight rule
Any signal report must use only information that would have been known at the signal timestamp. End-of-day results are reported separately from signal generation.

## Scope
- NIFTY 50
- BANKNIFTY
- All currently eligible NSE F&O stock underlyings
- Daily history first; intraday and option-contract studies next

## Data policy
Prefer NSE/broker/API data with documented timestamps. If data is unavailable or incomplete, the report must say so rather than fabricate values.
