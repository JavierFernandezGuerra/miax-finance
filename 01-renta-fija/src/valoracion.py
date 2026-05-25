"""Funciones de valoración de bonos y utilidades de apoyo."""

from datetime import datetime

import numpy as np
import pandas as pd


def yearfrac_act365(d1: datetime, d2: datetime) -> float:
    """Calcula año fraccional bajo convención ACT/365 simple."""
    return (d2 - d1).days / 365


def interpolate_discount_exp(curve_df: pd.DataFrame, target_date: datetime) -> float:
    """
    Interpolación exponencial estándar de mercado: interpolamos linealmente log(DF).
    Se espera que curve_df tenga índice de fechas y la columna "Discount".
    """
    dates = curve_df.index
    dfs = curve_df["Discount"].values

    t = np.array([(d - dates[0]).days / 365 for d in dates])
    log_df = np.log(dfs)

    t_target = (target_date - dates[0]).days / 365
    log_df_interp = np.interp(t_target, t, log_df)
    return float(np.exp(log_df_interp))


def generate_coupon_schedule(
    first_coupon: datetime, maturity: datetime, freq: int = 1
) -> list[datetime]:
    """Genera un calendario de cupones asumiendo frecuencia fija (por defecto anual)."""
    dates = []
    d = maturity
    while d >= first_coupon:
        dates.append(d)
        d = d.replace(year=d.year - 1)
    return sorted(dates)


def valorar_bono(
    isin: str,
    universo: pd.DataFrame,
    curva_estr: pd.DataFrame,
    fecha_valor: datetime = datetime(2025, 10, 1),
    spread: float = 0.0,
) -> dict:
    """
    Valora un bono aplicando, si procede, un spread de crédito.

    spread debe expresarse en puntos porcentuales (0.01 = 1 %).
    Devuelve un diccionario con precio sucio, cupón corrido y precio limpio.
    """
    row = universo.loc[isin]

    coupon_rate = float(row["Coupon"])
    freq = int(row["Coupon Frequency"])
    first_coupon = pd.to_datetime(row["First Coupon Date"], dayfirst=True, errors="coerce")

    next_call = row.get("Next Call Date")
    if pd.notnull(next_call):
        maturity = pd.to_datetime(next_call, dayfirst=True, errors="coerce")
    else:
        maturity = pd.to_datetime(row.get("Maturity"), dayfirst=True, errors="coerce")

    if pd.isna(first_coupon):
        first_coupon = fecha_valor
    if pd.isna(maturity):
        maturity = fecha_valor.replace(year=fecha_valor.year + 50)

    schedule = generate_coupon_schedule(first_coupon, maturity, freq)
    past = [d for d in schedule if d <= fecha_valor]
    future = [d for d in schedule if d > fecha_valor]

    last_coupon = past[-1] if past else first_coupon
    next_coupon = future[0] if future else maturity

    accrual_elapsed = yearfrac_act365(last_coupon, fecha_valor)
    accrued_coupon = coupon_rate * accrual_elapsed

    dirty_price = 0.0
    for d in future:
        df = interpolate_discount_exp(curva_estr, d)
        t = yearfrac_act365(fecha_valor, d)
        cf = coupon_rate
        if d == maturity:
            cf += 100  # principal
        cf_discounted = cf * df * np.exp(-spread * t)
        dirty_price += cf_discounted

    clean_price = dirty_price - accrued_coupon

    return {
        "precio_sucio": dirty_price,
        "cupón_corrido": accrued_coupon,
        "precio_limpio": clean_price,
        "ultimo_cupon": last_coupon,
        "siguiente_cupon": next_coupon,
    }


def valorar_universo(
    universo: pd.DataFrame,
    curva_estr: pd.DataFrame,
    precios_universo: pd.DataFrame,
    fecha_valor: datetime = datetime(2025, 10, 1),
) -> pd.DataFrame:
    """Valora todos los bonos del universo con spread=0 y devuelve resumen en DataFrame."""
    resultados = []

    for isin in universo.index:
        val = valorar_bono(isin, universo, curva_estr, fecha_valor, spread=0.0)
        try:
            mercado = precios_universo.loc[fecha_valor, f"{isin} Corp"]
        except KeyError:
            mercado = np.nan

        resultados.append(
            {
                "ISIN": isin,
                "precio_limpio_teorico": val["precio_limpio"],
                "precio_sucio_teorico": val["precio_sucio"],
                "cupon_corrido": val["cupón_corrido"],
                "precio_mercado": mercado,
                "diferencia": val["precio_limpio"] - mercado if pd.notnull(mercado) else np.nan,
            }
        )

    return pd.DataFrame(resultados).set_index("ISIN")

