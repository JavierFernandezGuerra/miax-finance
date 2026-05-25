# 04 — Risk Management: Regime-Aware Multi-Asset Stress Testing

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![Topic](https://img.shields.io/badge/topic-stress_testing-red)
![Status](https://img.shields.io/badge/status-completed-success)

> **TL;DR** — A stress-testing engine for a multi-asset US basket. Identify calm vs crisis regimes with an **HMM**, model dependence with **copulas**, and simulate **economically coherent** tail scenarios via Monte Carlo — fully interpretable, no opaque models.

## Why this approach

A parametric VaR fails in the exact moment it matters most: when markets break normality. Separating **regime + copula + tail** gives a tail-risk estimate that is **coherent with the data** without sacrificing traceability — every component can be inspected in isolation:

- The **HMM** explains *when* the market is fragile.
- The **copula** explains *how* assets co-move conditional on the regime.
- **Monte Carlo** propagates both through a non-Gaussian joint distribution.

## Pipeline

1. **Data** — daily returns for ETFs spanning the main macro blocks (equity, long bonds, gold, real estate, volatility, ...), pulled with `yfinance`.
2. **Regime model** — Gaussian HMM (`hmmlearn`) on standardised returns, splitting calm and crisis states.
3. **Copulas** — non-linear dependence modelled inside each regime, separating marginals from the dependence structure.
4. **Monte Carlo** — conditional paths per regime preserving fat tails and the captured dependence.
5. **Risk metrics** — simulated VaR / ES / drawdown, including crisis-regime stress scenarios.

## Repository layout

```
04-gestion-riesgos/
├── riesgos.ipynb
├── requirements.txt
└── README.md
```

## How to run

```bash
cd 04-gestion-riesgos
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab riesgos.ipynb
```

> The notebook downloads its inputs from `yfinance` on first run; no local data files required.
