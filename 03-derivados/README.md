# 03 — Derivatives: Delta-Hedged Long Straddle on SPY

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![IBKR](https://img.shields.io/badge/broker-Interactive_Brokers-blue)
![Status](https://img.shields.io/badge/status-completed-success)

> **TL;DR** — Periodic long-straddle on SPY: build the strategy, derive its own greeks, design a delta-hedged variant, simulate order routing (combo vs legged), and discuss delta-neutralisation with a second option.

## Objective

1. Build a **periodic long-straddle** on SPY.
2. Design the **delta-hedged** version computing greeks in-house.
3. Analyse the **historical P&L** of both variants.
4. Simulate order routing in two modes:
   - **Combo**: the straddle as a single ticket.
   - **Legged**: call and put as separate orders, quantifying the *legging risk* (mid-quote drift between fills).
5. **Delta-neutralise with a second option** and reason about the residual exposure in Gamma, Vega and Theta.
6. Discuss what would change using **SPX** (cash-settled, European) instead of SPY (physical, American).

## Modelling decision: simulated Black–Scholes

A retail Interactive Brokers paper account does **not allow consistent historical option chain downloads**. To keep the project reproducible:

- Option prices are simulated with **Black–Scholes**, using the **ATM IV** observed via the IBKR API as input.
- Spot, option chain, ATM IV, broker-side greeks and historical SPY closes are pulled **live from IBKR**.
- Locking option pricing to a closed-form model (instead of replaying live mid-quotes) keeps the focus on P&L attribution, delta-hedging and greek-by-greek decomposition — independent of broker data availability.

## IBKR connection

- A flag `EXECUTE_ORDERS = False` at the top of the notebook guards live order submission. **Keep it `False`** unless TWS / IB Gateway is running with paper-trading credentials.
- With `EXECUTE_ORDERS = True` and the standard local port, the notebook submits simulated orders (combo + legs) to the paper account.

## Repository layout

```
03-derivados/
├── delta_hedged_straddle_spy.ipynb
├── requirements.txt
└── README.md
```

## How to run

```bash
cd 03-derivados
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab delta_hedged_straddle_spy.ipynb
```

> Historical P&L and delta-hedge analysis work fully **offline** with the Black–Scholes simulation; the IBKR connection is only needed for the live order-routing demo.
