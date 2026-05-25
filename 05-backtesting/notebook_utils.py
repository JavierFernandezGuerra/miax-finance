"""Utilidades compartidas para notebooks de backtesting.

Este módulo concentra funciones reutilizables para:
- detectar rutas del proyecto,
- configurar visualización de pandas,
- validar y cargar ficheros.

El objetivo es mejorar modularidad, reutilización y legibilidad.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


@dataclass(frozen=True)
class ProjectPaths:
    """Contenedor inmutable de rutas clave del proyecto."""

    root: Path
    datasets: Path
    outputs: Path
    notebooks: Path


def detect_project_root(start_path: Optional[Path] = None) -> Path:
    """Detecta la raíz del proyecto a partir de la ruta actual.

    Busca hacia arriba un directorio que contenga `datasets` y `notebooks`.
    """
    current = (start_path or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        if (candidate / "datasets").exists() and (candidate / "notebooks").exists():
            return candidate

    raise FileNotFoundError(
        "No se pudo detectar la raíz del proyecto "
        "(se esperaban carpetas 'datasets' y 'notebooks')."
    )


def get_project_paths(start_path: Optional[Path] = None) -> ProjectPaths:
    """Devuelve rutas estándar del proyecto en una única estructura."""
    root = detect_project_root(start_path)
    return ProjectPaths(
        root=root,
        datasets=root / "datasets",
        outputs=root / "outputs",
        notebooks=root / "notebooks",
    )


def configure_notebook_display(
    max_columns: Optional[int] = None,
    max_rows: int = 100,
    width: Optional[int] = None,
    max_colwidth: Optional[int] = None,
) -> None:
    """Aplica una configuración de visualización homogénea para pandas."""
    pd.set_option("display.max_columns", max_columns)
    pd.set_option("display.max_rows", max_rows)
    pd.set_option("display.width", width)
    pd.set_option("display.max_colwidth", max_colwidth)


def load_parquet_checked(path: Path) -> pd.DataFrame:
    """Carga un parquet y valida que exista."""
    if not path.exists():
        raise FileNotFoundError(f"No existe el fichero parquet: {path}")
    return pd.read_parquet(path)


def ensure_datetime_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Convierte una columna a datetime y devuelve una copia segura."""
    out = df.copy()
    out[column] = pd.to_datetime(out[column])
    return out
