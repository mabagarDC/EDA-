"""Punto de entrada del proyecto «¿Quién dirige el cine?» (TMDB, 2000-2025).

Uso, desde la raíz del repositorio:

    python src/main.py --comprobar   # mira qué hay disponible, sin ejecutar nada
    python src/main.py --memoria     # ejecuta la memoria (solo necesita src/data/resultados/)
    python src/main.py               # ejecuta el análisis: notebooks 03a y 03b
    python src/main.py --direccion   # igual, pero antes rehace la tabla de dirección (02b)
    python src/main.py --orden       # muestra el orden completo de los notebooks

La descarga de datos (notebooks 00, 01, 01b y 02) NO se lanza desde aquí:
tarda unas 8 horas y necesita un token de TMDB. Se hace a mano, en el orden
que indica --orden. Los datos originales no están en el repositorio.
"""
import argparse
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
RAIZ = SRC.parent
NOTEBOOKS = SRC / "notebooks"
PROCESADOS = SRC / "data" / "processed"
CREDITOS = SRC / "data" / "raw" / "creditos"
RESULTADOS = SRC / "data" / "resultados"

ANALISIS = ["03a_analisis_visualizacion", "03b_comparacion_direccion"]

# Orden real de ejecución. El notebook 01 se ejecuta en dos partes porque la
# sección 6 lee un archivo que crea el notebook 02.
ORDEN = [
    ("00_pruebas_api", "Pruebas con la API de TMDB (necesita .env con TMDB_TOKEN)"),
    ("01_obtencion_datos", "Secciones 1 a 5: descarga de los listados de películas"),
    ("02_limpieza_datos", "Limpieza y preparación; guarda peliculas_preparadas.pkl"),
    ("01_obtencion_datos", "Sección 6: descarga de créditos (lee peliculas_preparadas.pkl)"),
    ("01b_revision_errores", "Revisión de los 32 errores 404 y de los archivos guardados"),
    ("02b_direccion", "Tabla de dirección y variable grupo_direccion"),
    ("03a_analisis_visualizacion", "Géneros y evolución de todo el catálogo"),
    ("03b_comparacion_direccion", "Comparación por grupo de dirección"),
]

# Archivos que necesita cada modo
NECESARIOS_ANALISIS = [
    PROCESADOS / "peliculas_preparadas.pkl",
    PROCESADOS / "peliculas_todas_con_grupo.pkl",
    PROCESADOS / "peliculas_con_direccion.pkl",
]


def necesarios_direccion():
    """02b necesita las películas preparadas y los créditos (o sus tramos ya leídos)."""
    rutas = [PROCESADOS / "peliculas_preparadas.pkl"]
    if not (PROCESADOS / "tramos_direccion").exists():
        rutas.append(CREDITOS)
    return rutas


def estado(ruta):
    return "sí" if ruta.exists() else "NO"


def mostrar_orden():
    print("Orden de ejecución de los notebooks (src/notebooks/):\n")
    for n, (nombre, descripcion) in enumerate(ORDEN, start=1):
        print(f"  {n}. {nombre}: {descripcion}")
    print("\nDesde main.py solo se lanzan los pasos 7 y 8 (y, con --direccion, el 6).")


def comprobar():
    print("Comprobación (no se ejecuta nada)\n")
    print(f"  .env en la raíz (lo necesitan los notebooks): {estado(RAIZ / '.env')}")
    print(f"  Resultados para la memoria (src/data/resultados/): {estado(RESULTADOS)}")
    print("\n  Datos para --direccion:")
    for ruta in necesarios_direccion():
        print(f"    {ruta.relative_to(RAIZ)}: {estado(ruta)}")
    print("    (basta con src/data/processed/tramos_direccion o con src/data/raw/creditos)")
    print("\n  Datos para el análisis (03a y 03b):")
    for ruta in NECESARIOS_ANALISIS:
        print(f"    {ruta.relative_to(RAIZ)}: {estado(ruta)}")


def faltan(rutas):
    return [r for r in rutas if not r.exists()]


def ejecutar(ruta_notebook):
    print(f"Ejecutando {ruta_notebook.name} ...", flush=True)
    comando = [
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook", "--execute", "--inplace",
        "--ExecutePreprocessor.timeout=-1",
        str(ruta_notebook),
    ]
    # cwd = carpeta del notebook: los notebooks buscan el .env hacia arriba
    resultado = subprocess.run(comando, cwd=ruta_notebook.parent)
    if resultado.returncode != 0:
        print(f"\nError al ejecutar {ruta_notebook.name}. "
              "¿Está instalado Jupyter? (pip install -r requirements.txt)")
        sys.exit(resultado.returncode)


def main():
    parser = argparse.ArgumentParser(description="Ejecuta el análisis del proyecto.")
    parser.add_argument("--comprobar", action="store_true",
                        help="muestra qué archivos hay disponibles y no ejecuta nada")
    parser.add_argument("--orden", action="store_true",
                        help="muestra el orden completo de los notebooks")
    parser.add_argument("--memoria", action="store_true",
                        help="ejecuta solo la memoria (src/memoria.ipynb)")
    parser.add_argument("--direccion", action="store_true",
                        help="rehace la tabla de dirección (02b) antes del análisis")
    args = parser.parse_args()

    if args.orden:
        mostrar_orden()
        return
    if args.comprobar:
        comprobar()
        return

    if args.memoria:
        if not RESULTADOS.exists():
            sys.exit("No existe src/data/resultados/. Sin esos CSV la memoria no puede leer nada.")
        ejecutar(SRC / "memoria.ipynb")
        return

    pasos = (["02b_direccion"] if args.direccion else []) + ANALISIS
    ausentes = faltan(necesarios_direccion() if args.direccion else NECESARIOS_ANALISIS)
    if not (RAIZ / ".env").exists():
        print("Aviso: no hay .env en la raíz. Los notebooks lo usan para localizar el "
              "proyecto; para el análisis basta con un archivo vacío.")
    if ausentes:
        print("Faltan estos datos, que no se incluyen en el repositorio:")
        for ruta in ausentes:
            print("  -", ruta.relative_to(RAIZ))
        print("\nPara generarlos hay que ejecutar los notebooks de descarga y limpieza "
              "(python src/main.py --orden).\nPara revisar los resultados sin datos: "
              "python src/main.py --memoria")
        sys.exit(1)

    for nombre in pasos:
        ejecutar(NOTEBOOKS / f"{nombre}.ipynb")
    print("\nTerminado. Las figuras están en figuras/ y los CSV en src/data/resultados/.")


if __name__ == "__main__":
    main()
