# ¿Quién dirige el cine? Mujeres en la dirección de películas (2000-2025)

Proyecto de análisis exploratorio de datos (EDA) del bootcamp de Data Science
de The Bridge. Autora: María Balagué García.

## De qué trata

Analiza las películas estrenadas entre 2000 y 2025 en TMDB (681.868) para
responder: **¿qué géneros dirigen más las mujeres y cómo ha cambiado su
presencia en 25 años?**

Resultados principales:

- Los hombres dirigen más en todos los géneros: el 78 % de las películas de
  dirección conocida frente al 20 % de mujeres y personas no binarias.
- La presencia de mujeres crece del 13,5 % (2000-04) al 24,2 % (2021-25).
  No es solo porque haya más películas: por cada 100 dirigidas por hombres,
  pasan de 15,8 a 32,7 de mujeres y personas no binarias (×5,8 frente a ×2,8).
- El drama es el género más frecuente para ambos grupos; lo que distingue a
  las directoras es el documental.
- Limitación principal: en el 53,6 % de las películas, TMDB no informa del
  género de la dirección.

## Contenido

| Qué | Dónde |
|---|---|
| Memoria (resumen de todo el proceso) | `src/memoria.ipynb` |
| Presentación | `Presentacion_EDA_TMDB.pptx` |
| Código completo, paso a paso | `src/notebooks/` |
| Punto de entrada | `src/main.py` |
| Funciones auxiliares | `src/utils/` |
| Resultados (CSV pequeños) | `src/data/resultados/` |
| Gráficas | `figuras/` |

```
├── README.md
├── requirements.txt
├── Presentacion_EDA_TMDB.pptx
├── figuras/
└── src/
    ├── main.py
    ├── memoria.ipynb
    ├── notebooks/
    ├── utils/
    └── data/
        └── resultados/
```

Los datos originales y los intermedios (`src/data/raw/` y `src/data/processed/`)
no se incluyen en el repositorio: son cientos de miles de archivos.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python src/main.py --comprobar   # qué hay disponible, sin ejecutar nada
python src/main.py --memoria     # la memoria, sin necesitar los datos originales
python src/main.py               # el análisis (notebooks 03a y 03b), con los datos
python src/main.py --orden       # orden completo de los notebooks
```

Para revisar el proyecto sin datos basta con abrir `src/memoria.ipynb`: lee los
CSV de `src/data/resultados/`.

Los notebooks localizan el proyecto buscando un archivo `.env` en la raíz.
Para repetir la descarga hace falta una cuenta de TMDB y `TMDB_TOKEN=<tu token>`
dentro de ese archivo; para el análisis basta con que exista, aunque esté vacío.

## Orden de ejecución de los notebooks

| Orden | Notebook | Qué hace |
|---|---|---|
| 1 | `00_pruebas_api` | Pruebas con la API de TMDB |
| 2 | `01_obtencion_datos` (secciones 1-5) | Descarga de los listados de películas |
| 3 | `02_limpieza_datos` | Limpieza; guarda `peliculas_preparadas.pkl` |
| 4 | `01_obtencion_datos` (sección 6) | Descarga de créditos (lee el archivo del paso 3) |
| 5 | `01b_revision_errores` | Revisión de los 32 errores 404 |
| 6 | `02b_direccion` | Variable `grupo_direccion` |
| 7 | `03a_analisis_visualizacion` | Géneros y evolución del catálogo |
| 8 | `03b_comparacion_direccion` | Comparación por grupo de dirección |

El notebook 01 se ejecuta en dos partes porque su sección 6 necesita un archivo
que crea el notebook 02. La descarga completa de créditos tarda unas 8 horas,
por eso los notebooks 01 y 01b tienen un interruptor (`EJECUTAR_... = False`)
para no repetirla por error.

## Decisiones y limitaciones

- **No se comparan valoraciones.** El 60,79 % de las películas no tiene ningún
  voto, así que su valoración no existe. El número de votos se usa como nivel
  de visibilidad (todas, al menos 1 voto, al menos 100 votos).
- **Regla conservadora de dirección:** si algún director tiene el género sin
  especificar, la película va a «No identificado».
- **El género procede de TMDB**, no es una autoidentificación verificada.
- **El descarte de películas sin director no es aleatorio**; el análisis
  describe las películas con dirección registrada en TMDB.

## Tecnologías

Python · pandas · numpy · matplotlib · requests · python-dotenv · Jupyter ·
hilos (`concurrent.futures`) para la descarga en paralelo.

Datos: [TMDB](https://www.themoviedb.org/). Este producto usa la API de TMDB
pero no está avalado ni certificado por TMDB.
