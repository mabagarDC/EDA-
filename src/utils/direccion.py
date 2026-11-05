"""Funciones auxiliares para el análisis de la dirección de las películas.

Se usan en `src/memoria.ipynb`. La misma lógica de clasificación está en el
notebook `02b_direccion`, que es donde se aplicó a los datos completos.
"""
from pathlib import Path

import pandas as pd


def clasificar_direccion(codigos):
    """Clasifica una película según los códigos de género de sus directores.

    Códigos de TMDB: 0 = sin especificar, 1 = mujer, 2 = hombre, 3 = no binaria.

    - Si alguna persona tiene el código 0, la película es «No identificado»
      (no se puede saber si el equipo es de mujeres, de hombres o mixto).
    - Solo códigos 1 y 3: «Mujeres» (incluye personas no binarias).
    - Solo código 2: «Hombres».
    - Códigos de ambos grupos: «Mixto».
    """
    codigos = set(codigos)
    if 0 in codigos:
        return "No identificado"
    hay_mujer = bool(codigos & {1, 3})
    hay_hombre = 2 in codigos
    if hay_mujer and hay_hombre:
        return "Mixto"
    if hay_mujer:
        return "Mujeres"
    return "Hombres"


def intervalo_confianza_95(n_exitos, n):
    """Semiancho (en puntos porcentuales) del intervalo de confianza al 95 %
    de una proporción, con la aproximación normal."""
    if n == 0:
        return float("nan")
    p = n_exitos / n
    return 1.96 * (p * (1 - p) / n) ** 0.5 * 100


def formato_miles(numero):
    """Formatea un número con punto como separador de miles (1.234.567)."""
    return f"{numero:,.0f}".replace(",", ".")


def buscar_raiz(inicio=None):
    """Sube por las carpetas hasta encontrar la que contiene `figuras/`."""
    actual = Path(inicio or Path.cwd()).resolve()
    for carpeta in [actual, *actual.parents]:
        if (carpeta / "figuras").is_dir():
            return carpeta
    raise FileNotFoundError("No se encuentra la carpeta del proyecto (con `figuras/`).")


def leer_resultado(nombre, raiz=None):
    """Lee un CSV de `src/data/resultados/` (codificado en utf-8-sig)."""
    raiz = raiz or buscar_raiz()
    return pd.read_csv(raiz / "src" / "data" / "resultados" / nombre, encoding="utf-8-sig")
