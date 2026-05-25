# 07 — Fund of Funds Tilted to Asia ex Japan

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![scikit-learn](https://img.shields.io/badge/scikit_learn-1.3+-orange)
![Topic](https://img.shields.io/badge/topic-asset_allocation-purple)
![Status](https://img.shields.io/badge/status-completed-success)

> **TL;DR** — Quantitative design of a **Fund of Funds (FoF)** with a structural tilt to **Asia ex Japan** equities. The mandate prioritises **factor replication** of the regional market rather than alpha picking. Methodological work — not investment advice.

---

## Pipeline

1. **Data quality** — trading calendar aligned with the factor source, point-imputation, exclusion of funds with insufficient coverage or extreme cross-sectional return behaviour (IQR-based filters). Log-returns in excess of the risk-free rate where appropriate.

2. **Per-fund feature vector** — **multi-window OLS** (1, 3 and 5 years) against the four **Fama–French** regional factors (Mkt-RF, SMB, HML, MOM) for Asia ex Japan. For each fund the pipeline computes:
   - **Betas and alphas** by window, with direct economic reading.
   - **Bull vs bear regime betas**.
   - **Risk/return metrics**: volatility, skew, tail measures, drawdown, Sharpe, Sortino, implicit tracking error vs the factor model, temporal stability of coefficients.
   - Coefficients are **shrunk when the t-statistic is weak** via `β_adj = β · (1 − exp(−|t|))`, so the learning input is not dominated by statistical noise.

3. **Asia-tilt filter** — universe restriction based on factor-model fit quality and significance of the market beta.

4. **PCA + Clustering** — on the standardised feature matrix:
   - **PCA** up to ~90% cumulative explained variance — kills the redundancy typical of correlated financial features.
   - **K-means** (elbow + silhouette).
   - **Hierarchical agglomerative (HAC)** with Ward linkage.
   - The two partitions are compared and reconciled.

5. **Visual exploration with Graphext** — export of the reduced space to inspect the similarity network across funds.

   ![K-means clusters in Graphext](k_means_graphext.png)
   ![HAC clusters in Graphext](HAC_graphext.png)

6. **FoF construction** — selection of the cluster best aligned with the indexing mandate via a scoring function combining market exposure, factor-fit quality and residual dispersion. A core (`top-N`) is defined with weights proportional to a factor score, renormalised daily by data availability.

7. **Final validation with AAXJ** — the **iShares MSCI All Country Asia ex Japan ETF** is **strictly reserved** for the ex-post check (correlation, tracking error, beta). It is **not used** for selection, clustering or weighting.

## Data

- **Daily NAVs** of ~25,000 funds provided by **IronIA** via `navs.pickle` (not redistributed, proprietary). Window 2016-01-05 → 2021-07-16.
- **Fama-French Asia ex Japan factors** from the [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).
- **AAXJ ETF** via `yfinance`, for the final validation step only.

The repository ships `graphext_funds_clustering.csv` with the funds in the selected cluster plus their features, ready for external inspection.

## Repository layout

```
07-fondo-de-fondos/
├── fondo_sesgado_asia.ipynb
├── graphext_funds_clustering.csv     # final export for Graphext
├── HAC_graphext.png                   # figures used in this README
├── k_means_graphext.png
├── requirements.txt
└── README.md
```

## How to run

```bash
cd 07-fondo-de-fondos
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab fondo_sesgado_asia.ipynb
```

> The IronIA NAVs file (`navs.pickle`) is proprietary and not included. Without it the notebook is only readable; the AAXJ validation block is independently reproducible via `yfinance`.
