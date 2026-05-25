# Quantitative Finance Studies

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Notebooks](https://img.shields.io/badge/jupyter-notebooks-orange)
![Status](https://img.shields.io/badge/status-completed-success)

A collection of self-contained studies in **quantitative finance** spanning the technical stack expected of a junior quant: bond valuation and portfolio construction, equity market microstructure, options strategies, regime-aware risk management, realistic backtesting, ML-aware data preprocessing, and fund-of-funds construction with unsupervised learning.

Each subproject is a stand-alone repository with its own `README.md`, `requirements.txt`, and notebooks; raw data is not committed (downloaded on the fly when possible, or documented in each project's README).

## Contents

| # | Project | Topic | Core techniques |
|---|---------|-------|------------------|
| 01 | [`01-renta-fija/`](01-renta-fija/) | EUR corporate bond portfolio: valuation, z-spread, duration/convexity, constrained construction and hedging | Cashflow valuation, ESTR curve, `PuLP` LP, ITRAXX / Bund-futures hedging |
| 02 | [`02-renta-variable/`](02-renta-variable/) | High-frequency arbitrage on Spanish equities across fragmented venues (BME, CBOE, Turquoise, Aquis) | Consolidated tape, rising-edge detection, latency simulation |
| 03 | [`03-derivados/`](03-derivados/) | Periodic long-straddle on SPY with self-computed delta-hedge and order-routing simulation | Black–Scholes, custom greeks, Interactive Brokers API |
| 04 | [`04-gestion-riesgos/`](04-gestion-riesgos/) | Multi-asset stress testing with regime switching | Gaussian HMM (`hmmlearn`), copulas, Monte Carlo |
| 05 | [`05-backtesting/`](05-backtesting/) | Modular momentum backtest on the S&P 500 with realistic costs and Monte Carlo robustness | 5-step pipeline, `pyarrow`, MC simulation (30M paths) |
| 06 | [`06-preprocesado-ml/`](06-preprocesado-ml/) | López de Prado preprocessing toolkit for financial ML (alt. bars, fractional differentiation, denoised covariance, triple-barrier labelling, purged K-Fold) | Marcos López de Prado — _Advances in Financial Machine Learning_ |
| 07 | [`07-fondo-de-fondos/`](07-fondo-de-fondos/) | Fund-of-funds tilted to Asia ex Japan: factor exposure → PCA → clustering → portfolio | Fama–French multi-window, PCA, K-means, HAC, Graphext |

The AI-side projects of this body of work live in their own repositories:

- **[`miax-bayesian-networks`](https://github.com/JavierFernandezGuerra/miax-bayesian-networks)** — DAG-based causal discovery on macro returns; reproduces the _factor mirage_ from López de Prado & Zoonekynd (2025).
- **[`miax-neural-networks`](https://github.com/JavierFernandezGuerra/miax-neural-networks)** — Deep learning for S&P 500 return forecasting (64 model variants across MLP / RNN / CNN / mixed architectures) and a model-driven portfolio backtest on 2025.

## How to navigate

Each subproject is independent. The typical flow is:

```bash
git clone https://github.com/JavierFernandezGuerra/miax-finance.git
cd miax-finance/05-backtesting          # or any other
python -m venv .venv
.venv\Scripts\activate                   # Windows
pip install -r requirements.txt
jupyter lab
```

Notebooks are written to be executed linearly (_Restart & Run All_). When a project requires external data that cannot be redistributed, the project's `README.md` documents how to obtain it.

## Repository layout

```
miax-finance/
├── 01-renta-fija/              # corporate-bond portfolio with LP optimisation
├── 02-renta-variable/          # HF arbitrage across fragmented venues
├── 03-derivados/               # delta-hedged straddle on SPY (BS + IBKR)
├── 04-gestion-riesgos/         # HMM + copulas + Monte Carlo stress testing
├── 05-backtesting/             # S&P 500 momentum pipeline
├── 06-preprocesado-ml/         # López de Prado financial-ML preprocessing
├── 07-fondo-de-fondos/         # Asia ex-Japan FoF with clustering
├── .gitignore
├── LICENSE                     # MIT
└── README.md                   # this file
```

## License

[MIT](LICENSE)
