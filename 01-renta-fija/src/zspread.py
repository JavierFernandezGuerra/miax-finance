"""Herramientas para cálculo y visualización de Z-spreads."""

from datetime import datetime
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.optimize import brentq
from tqdm import tqdm

from valoracion import valorar_bono


def calcular_zspread(
    isin: str,
    universo: pd.DataFrame,
    curva_estr: pd.DataFrame,
    precio_mercado: float,
    fecha_valor: datetime = datetime(2025, 10, 1),
) -> float:
    """Calcula el Z-spread (en bps) que iguala precio teórico y precio de mercado."""

    def precio_diff(spread: float) -> float:
        val = valorar_bono(isin, universo, curva_estr, fecha_valor, spread)
        return val["precio_limpio"] - precio_mercado

    try:
        z = brentq(precio_diff, 0.0, 0.2)
    except ValueError:
        return np.nan

    return z * 10000


def plot_parallel_shift(
    curva_base: pd.DataFrame,
    df_zspreads: pd.DataFrame,
    fecha_valor: datetime,
    modo: str = "global",
    isin_bonos: Sequence[str] | None = None,
    figsize: tuple[int, int] = (10, 6),
) -> None:
    """Grafica la curva base y su desplazamiento aplicando Z-spreads."""
    curva = curva_base.copy()
    curva.index = pd.to_datetime(curva.index, dayfirst=True)

    curva["t"] = (curva.index - pd.Timestamp(fecha_valor)).days / 365
    t = curva["t"]
    r_base = curva["Zero Rate"]

    plt.figure(figsize=figsize)
    plt.plot(t, r_base * 100, label="Curva base (Zero Rate)", color="cyan", linewidth=2)

    if modo == "global":
        zspread_promedio = df_zspreads["ZSpread_bps"].mean() / 10000
        r_shifted = r_base + zspread_promedio
        plt.plot(
            t,
            r_shifted * 100,
            label=f"Curva + Z-spread promedio ({zspread_promedio*100:.2f}%)",
            color="darkorange",
            linestyle="--",
            linewidth=2,
        )
    elif modo == "individual":
        if isin_bonos is None:
            raise ValueError("Para modo='individual', debe especificarse el parámetro isin_bonos.")

        if isinstance(isin_bonos, str):
            isin_bonos = [isin_bonos]

        colors = plt.cm.tab10.colors
        for i, isin_bono in enumerate(isin_bonos):
            if isin_bono not in df_zspreads.index:
                raise ValueError(f"ISIN {isin_bono} no encontrado en df_zspreads.")
            z = df_zspreads.loc[isin_bono, "ZSpread_bps"] / 10000
            r_shifted = r_base + z
            plt.plot(
                t,
                r_shifted * 100,
                label=f"{isin_bono} (+{z*100:.2f}%)",
                color=colors[i % len(colors)],
                linestyle="--",
                linewidth=2,
            )
    else:
        raise ValueError("modo debe ser 'global' o 'individual'")

    plt.xlabel("Tiempo hasta vencimiento (años)")
    plt.ylabel("Tasa cero (%)")
    plt.title(f"Shift paralelo de la curva - modo: {modo}")
    plt.grid(True)
    plt.legend()
    plt.show()


def evaluar_zspread(
    universo: pd.DataFrame,
    df_zspreads: pd.DataFrame,
    curva_estr: pd.DataFrame,
    precios_universo: pd.DataFrame,
    fecha_valor: datetime,
    bins: int = 30,
    rango_hist: tuple[float, float] = (-0.5, 0.5),
    decimales: int = 4,
) -> pd.DataFrame:
    """Valora todos los bonos aplicando sus Z-spreads y resume diferencias vs mercado."""
    resultados_ajustados = []

    for isin in tqdm(universo.index):
        z = df_zspreads.loc[isin, "ZSpread_bps"]

        if pd.isnull(z):
            resultados_ajustados.append(
                {"ISIN": isin, "precio_ajustado": np.nan, "precio_mercado": np.nan, "diff": np.nan}
            )
            continue

        spread_decimal = z / 10000
        val = valorar_bono(isin, universo, curva_estr, fecha_valor, spread=spread_decimal)

        try:
            precio_mercado = precios_universo.get(f"{isin} Corp", pd.Series()).get(
                pd.Timestamp(fecha_valor), np.nan
            )
        except KeyError:
            precio_mercado = np.nan

        resultados_ajustados.append(
            {
                "ISIN": isin,
                "precio_ajustado": val["precio_limpio"],
                "precio_mercado": precio_mercado,
                "diff": val["precio_limpio"] - precio_mercado if pd.notnull(precio_mercado) else np.nan,
            }
        )

    df_ajustado = pd.DataFrame(resultados_ajustados).set_index("ISIN")
    df_ajustado["diff_round"] = df_ajustado["diff"].round(decimales)
    df_ajustado.loc[np.abs(df_ajustado["diff_round"]) < 10 ** (-decimales), "diff_round"] = 0

    print("\nDiferencia media ajustada:", df_ajustado["diff_round"].mean())
    print("Diferencia máxima ajustada:", df_ajustado["diff_round"].max())
    print("Diferencia mínima ajustada:", df_ajustado["diff_round"].min())

    df_ajustado["diff_bps"] = df_ajustado["diff"] * 100
    plt.figure(figsize=(8, 5))
    df_ajustado["diff_bps"].dropna().hist(bins=bins, range=rango_hist)
    plt.xlabel("Diferencia ajustada (bps)")
    plt.ylabel("Número de bonos")
    plt.title("Diferencias tras aplicar Z-spread (escala bps)")
    plt.grid(True)
    plt.show()

    return df_ajustado


def plot_zspread_by_rating_extended(
    universo: pd.DataFrame,
    df_zspreads: pd.DataFrame,
    sector: str = "Financial",
    rating_order: Iterable[str] | None = None,
    seed: int = 42,
    figsize: tuple[int, int] = (12, 6),
    color_by_size: bool = False,
) -> None:
    """Grafica Z-spreads por rating para un sector concreto."""
    df_comparacion = universo.copy()
    df_comparacion["ZSpread_bps"] = df_zspreads["ZSpread_bps"]

    df_comparacion = df_comparacion[
        (df_comparacion["ZSpread_bps"].notnull()) & (df_comparacion["Industry Sector"] == sector)
    ].copy()

    def sample_one(df: pd.DataFrame) -> pd.DataFrame:
        return df.sample(1, random_state=seed)

    bonos_por_rating = df_comparacion.groupby("Rating", group_keys=False, dropna=False).apply(sample_one)

    cols = ["Coupon", "Maturity", "Next Call Date", "Outstanding Amount", "ZSpread_bps", "Rating"]
    df_repr = bonos_por_rating[cols].copy()
    df_repr["Composite Rating"] = df_repr["Rating"].astype(str)

    if rating_order is None:
        rating_order = [
            "AA+",
            "AA",
            "AA-",
            "A+",
            "A",
            "A-",
            "BBB+",
            "BBB",
            "BBB-",
            "BB+",
            "B+",
            "B",
            "B-",
            "CCC",
        ]
    existing_ratings = df_repr["Composite Rating"].unique()
    rating_order_filtered = [r for r in rating_order if r in existing_ratings]
    df_repr["Composite Rating"] = pd.Categorical(
        df_repr["Composite Rating"], categories=rating_order_filtered, ordered=True
    )
    df_repr = df_repr.sort_values("Composite Rating").reset_index(drop=True)

    plt.figure(figsize=figsize)

    if color_by_size:
        sns.barplot(
            x="Composite Rating",
            y="ZSpread_bps",
            data=df_repr,
            hue="Outstanding Amount",
            dodge=False,
            palette="viridis",
        )
        plt.legend(title="Outstanding Amount")
    else:
        sns.barplot(x="Composite Rating", y="ZSpread_bps", data=df_repr, color="steelblue")
        plt.legend([], [], frameon=False)

    plt.xlabel("Composite Rating")
    plt.ylabel("Z-Spread (bps)")
    plt.title(f"Z-Spread por Rating - Sector {sector}")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


def plot_extremos_parallel_shift(
    curva_base: pd.DataFrame,
    df_zspreads: pd.DataFrame,
    fecha_valor: datetime,
    figsize: tuple[int, int] = (10, 6),
) -> None:
    """Grafica curvas ajustadas para los bonos con Z-spread máximo, mediano y mínimo."""
    df_valid = df_zspreads[df_zspreads["ZSpread_bps"].notna()]

    isin_max = df_valid["ZSpread_bps"].idxmax()
    max_zspread = df_valid.loc[isin_max, "ZSpread_bps"]

    isin_min = df_valid["ZSpread_bps"].idxmin()
    min_zspread = df_valid.loc[isin_min, "ZSpread_bps"]

    median_value = df_valid["ZSpread_bps"].median()
    isin_median = (df_valid["ZSpread_bps"] - median_value).abs().idxmin()
    median_zspread = df_valid.loc[isin_median, "ZSpread_bps"]

    print(f"Mayor Z-spread: ISIN={isin_max}, Z={max_zspread:.2f} bps")
    print(f"Z-spread mediano: ISIN={isin_median}, Z={median_zspread:.2f} bps")
    print(f"Menor Z-spread: ISIN={isin_min}, Z={min_zspread:.2f} bps")

    plot_parallel_shift(
        curva_base=curva_base,
        df_zspreads=df_zspreads,
        fecha_valor=fecha_valor,
        modo="individual",
        isin_bonos=[isin_max, isin_median, isin_min],
        figsize=figsize,
    )

