# 05 — Backtesting: S&P 500 Momentum with Realistic Execution Costs

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![PyArrow](https://img.shields.io/badge/storage-pyarrow-yellow)
![Status](https://img.shields.io/badge/status-completed-success)

> **TL;DR** — A modular five-step pipeline for a cross-sectional momentum strategy on the S&P 500, including survivorship-aware data handling, trading costs, and a 30 M-path Monte Carlo robustness test. The exercise concludes with an **honest under-performance vs SPY** when costs are properly accounted for — exactly the result a serious backtest is supposed to produce.

## Pipeline (`notebooks/`)

| Notebook | Content |
|----------|---------|
| `01_Carga_Datos.ipynb` | S&P 500 price history + index membership; SPY benchmark. |
| `02_EDA_Preparacion.ipynb` | Cleaning, normalisation, survivorship-bias handling, reproducible panel. |
| `03_Estrategia_Momentum.ipynb` | Cross-sectional top-K selection by momentum; weight series generation. |
| `04_Backtest_Ejecucion_Costes.ipynb` | Realistic backtest with trading costs and turnover; outputs in `outputs/`. |
| `05_Comparativa_Metricas_MonteCarlo.ipynb` | Strategy vs SPY metrics + 30 M-path Monte Carlo. |

Shared utilities (display setup, project-wide `PATHS` class) live in `notebook_utils.py` and are imported at the top of every notebook.

## Results

After applying realistic trading costs and turnover, the momentum strategy **lagged a passive SPY position**:

| Strategy | CAGR | Sharpe | Sortino | Max DD | β vs SPY | α vs SPY |
|---|---:|---:|---:|---:|---:|---:|
| Momentum (this study) | 4.22% | 0.29 | 0.36 | −55.5% | 1.07 | −7.98% |
| SPY buy & hold | 13.51% | 0.80 | 0.98 | −33.7% | 1.00 | 0.00% |

Monte Carlo robustness (30 M random portfolios with the same constraints):

| Quantity | Value |
|---|---:|
| Median terminal equity | 405,007 |
| 5th percentile | 297,763 |
| 95th percentile | 550,532 |
| Algorithm terminal equity | 395,006 |

The strategy lands **near the Monte Carlo median**, confirming that the realised result is not a statistical fluke — it is what the strategy class is statistically expected to deliver under these constraints.

> Why ship this result publicly? Because most published "momentum beats SPY" backtests evaporate once execution costs, slippage and survivorship are modelled correctly. Reproducing the realistic version of the experiment is, in the author's view, more useful than another in-sample story.

## Outputs

`outputs/` ships with the artefacts produced by the pipeline:

- `portfolio_daily_equity.csv` — daily equity curve of the strategy.
- `benchmark_daily_equity.csv` — daily equity curve of SPY.
- `trades_detail.csv` — trade log with attributed cost per fill.
- `selected_assets.csv` — top-K selected on each rebalance date.
- `metrics_comparativa.csv` — risk/return metrics, strategy vs benchmark.
- `monte_carlo_summary.csv` — distribution of terminal equities under the MC.

## Repository layout

```
05-backtesting/
├── notebooks/
│   ├── 01_Carga_Datos.ipynb
│   ├── 02_EDA_Preparacion.ipynb
│   ├── 03_Estrategia_Momentum.ipynb
│   ├── 04_Backtest_Ejecucion_Costes.ipynb
│   └── 05_Comparativa_Metricas_MonteCarlo.ipynb
├── outputs/                  # CSVs produced by the pipeline
├── notebook_utils.py         # shared display + paths
├── requirements.txt
└── README.md
```

## How to run

```bash
cd 05-backtesting
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Run notebooks in order (`01 → 05`). Data is downloaded in `01_Carga_Datos.ipynb`.
