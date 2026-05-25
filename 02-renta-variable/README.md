# 02 — Equities: HF Arbitrage Across Fragmented Venues

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![Topic](https://img.shields.io/badge/topic-market_microstructure-purple)
![Status](https://img.shields.io/badge/status-completed-success)

> **TL;DR** — Detection and post-mortem of arbitrage opportunities on Spanish equities listed simultaneously on **BME, CBOE, Turquoise and Aquis**, quantifying how much of the theoretical edge survives realistic latency.

## Objective

Given tick-level quotes (`QTE`) and trading-status messages (`STS`) from the four venues:

1. Build a **consolidated tape** that aligns prices by timestamp across venues.
2. **Detect arbitrage signals** when `max(Bid) > min(Ask)` between venues (crossed book).
3. **Simulate latency degradation** in execution — how much spread is lost as a function of round-trip delay.
4. **Cross-validate** the results with a complementary simulation based on limit orders.

## Assumptions

- Trading only during **continuous-auction phases** (filtered with venue-specific `STS` status codes).
- Magic numbers (special price codes representing non-tradeable states) are filtered out.
- Only **level 0** (best bid / best ask) is used.
- **Rising-edge** logic prevents persistent opportunities from being counted as multiple events.

## Data

Tick data is proprietary and not redistributed. The notebook documents the expected schema so any feed with the same structure is processable end-to-end.

## Repository layout

```
02-renta-variable/
├── arbitrage_notebook.ipynb
├── requirements.txt
└── README.md
```

## How to run

```bash
cd 02-renta-variable
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab arbitrage_notebook.ipynb
```
