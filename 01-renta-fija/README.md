# 01 — Fixed Income: Corporate Bond Portfolio Construction

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![PuLP](https://img.shields.io/badge/optimisation-PuLP-orange)
![Status](https://img.shields.io/badge/status-completed-success)

> **TL;DR** — Valuation, risk metrics and constrained portfolio construction over a universe of EUR corporate bonds, with explicit hedging discussion for both interest-rate and credit risk.

## Objective

Build a corporate-bond portfolio of **at most 20 issues** that maximises total expected return subject to a realistic set of mandate constraints:

- Portfolio duration **≤ 3 years**.
- HY (high-yield) exposure **≤ 10%** of capital.
- **No subordinated** debt.
- **No issues ≤ €500 M** in size.
- **≤ 10%** of capital in a single issue.
- **≤ 15%** concentration per issuer.

The optimisation is formulated as a **linear programme** over fractional weights and solved with `PuLP`.

## Methodology

1. **Universe analysis** — coupon types, callability, subordination, rating, issue size; cleaning and feature engineering on the issue characteristics.
2. **Valuation** — discounted-cashflow pricing against the **ESTR curve** plus a credit spread (`src/valoracion.py`).
3. **Z-spread** — solved as a parallel shift over the curve that recovers the observed market price (`src/zspread.py`).
4. **Risk metrics** — yield, modified duration and convexity at instrument level.
5. **Equal-weight portfolio** vs the **RECMTREU** total-return benchmark, with backtest discussion.
6. **Constrained portfolio** — LP with the six mandate constraints; sensitivity to additional restrictions is discussed.
7. **Risk management** — credit risk (ITRAXX Main / XOVER) and interest-rate risk (Schatz / Bobl / Bund futures); how to size each hedge from portfolio Greeks.
8. **Relative-value strategy** — discussion of a value-tilted construction on top of the optimised portfolio.

## Data

Raw inputs (`universo.csv`, `precios_historicos_universo.csv`, `curvaESTR.csv`, `precios_varios.csv`) come from a proprietary feed and are **not redistributed**. The repository contains the code and the **selected portfolio output** (`outputs/selected_portfolio.csv`); to reproduce the full pipeline a compatible dataset is required.

## Repository layout

```
01-renta-fija/
├── notebooks/
│   └── analisis_cartera_renta_fija.ipynb
├── src/
│   ├── funciones.py          # universe-cleaning utilities
│   ├── valoracion.py         # DCF bond pricing
│   └── zspread.py            # z-spread solver
├── outputs/
│   └── selected_portfolio.csv
├── requirements.txt
└── README.md
```

## How to run

```bash
cd 01-renta-fija
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab notebooks/analisis_cartera_renta_fija.ipynb
```

> The notebook automatically prepends `src/` to `sys.path` so `funciones`, `valoracion` and `zspread` are importable from the standard kernel.
