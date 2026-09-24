"""
01_download_bts.py
Ingesta de BTS TranStats – Reporting Carrier On-Time Performance.

Qué hace, mes por mes:
  1. Descarga el ZIP oficial de BTS (se salta los que ya existen).
  2. Verifica que el ZIP no esté corrupto.
  3. Lee solo las columnas necesarias y guarda un Parquet por mes.
  4. Valida el archivo y agrega una fila a docs/ingestion_log.csv.

Los ZIP crudos NO se modifican (data/raw/). El resultado va a data/interim/.
Uso:  python 01_download_bts.py      (o ejecutar las celdas en Jupyter)
Requiere: pandas, requests, pyarrow   ->  pip install pandas requests pyarrow
"""

import io
import time
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

# ---------------------------------------------------------------- CONFIGURACIÓN
PERIODOS = [(2025, m) for m in range(7, 13)] + [(2026, m) for m in range(1, 7)]  # jul-2025 a jun-2026

BASE_URL = ("https://transtats.bts.gov/PREZIP/"
            "On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip")

ROOT = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
RAW_DIR = ROOT / "data" / "raw"
INTERIM_DIR = ROOT / "data" / "interim"
LOG_FILE = ROOT / "docs" / "ingestion_log.csv"

# Aerolíneas cliente (código IATA del reporting carrier)
CLIENTES = {"AA": "American", "DL": "Delta", "UA": "United", "B6": "JetBlue", "WN": "Southwest"}

COLUMNAS = [
    "Year", "Month", "DayofMonth", "DayOfWeek", "FlightDate",
    "Reporting_Airline", "Flight_Number_Reporting_Airline", "Tail_Number",
    "Origin", "OriginCityName", "OriginState", "Dest", "DestCityName", "DestState",
    "CRSDepTime", "DepTime", "DepDelay", "DepDel15",
    "CRSArrTime", "ArrTime", "ArrDelay", "ArrDel15",
    "Cancelled", "CancellationCode", "Diverted", "Distance",
    "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay",
]
# Horas como texto para no perder ceros a la izquierda (0605 ≠ 605)
TIPOS_TEXTO = {c: "string" for c in ["Reporting_Airline", "Flight_Number_Reporting_Airline",
               "Tail_Number", "Origin", "Dest", "CancellationCode",
               "CRSDepTime", "DepTime", "CRSArrTime", "ArrTime"]}

REINTENTOS = 4
TIMEOUT = 120  # segundos; el servidor de BTS es lento y a veces corta la conexión


# ---------------------------------------------------------------- FUNCIONES
def descargar(year: int, month: int) -> Path:
    """Descarga el ZIP del mes si no existe. Reintenta con espera creciente."""
    destino = RAW_DIR / f"ontime_{year}_{month:02d}.zip"
    if destino.exists() and zipfile.is_zipfile(destino):
        print(f"  ✓ ya existe: {destino.name}")
        return destino

    url = BASE_URL.format(year=year, month=month)
    temporal = destino.with_suffix(".part")
    for intento in range(1, REINTENTOS + 1):
        try:
            print(f"  ↓ descargando {year}-{month:02d} (intento {intento})...")
            with requests.get(url, stream=True, timeout=TIMEOUT) as r:
                r.raise_for_status()
                with open(temporal, "wb") as f:
                    for bloque in r.iter_content(chunk_size=1024 * 1024):
                        f.write(bloque)
            if not zipfile.is_zipfile(temporal):
                raise ValueError("el archivo descargado no es un ZIP válido "
                                 "(¿el mes aún no está publicado?)")
            temporal.replace(destino)
            return destino
        except Exception as e:
            print(f"    ✗ {e}")
            temporal.unlink(missing_ok=True)
            if intento < REINTENTOS:
                time.sleep(10 * intento)
    raise RuntimeError(f"No se pudo descargar {year}-{month:02d} tras {REINTENTOS} intentos: {url}")


def leer_zip(ruta_zip: Path) -> pd.DataFrame:
    """Verifica integridad y lee solo las columnas del proyecto."""
    with zipfile.ZipFile(ruta_zip) as z:
        corrupto = z.testzip()
        if corrupto:
            raise ValueError(f"ZIP corrupto en {corrupto}")
        csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if len(csvs) != 1:
            raise ValueError(f"Se esperaba 1 CSV y hay {len(csvs)}: {csvs}")
        with z.open(csvs[0]) as f:
            encabezado = pd.read_csv(f, nrows=0).columns
        faltantes = [c for c in COLUMNAS if c not in encabezado]
        if faltantes:
            raise ValueError(f"Faltan columnas en el archivo de BTS: {faltantes}")
        with z.open(csvs[0]) as f:
            return pd.read_csv(f, usecols=COLUMNAS, dtype=TIPOS_TEXTO, low_memory=False)


def validar(df: pd.DataFrame, year: int, month: int) -> dict:
    """Controles de calidad. Devuelve un resumen para el log de auditoría."""
    errores = []
    periodos = set(zip(df["Year"], df["Month"]))
    if periodos != {(year, month)}:
        errores.append(f"período inesperado {periodos}")
    if df.duplicated(["FlightDate", "Reporting_Airline", "Flight_Number_Reporting_Airline",
                      "Origin", "Dest", "CRSDepTime"]).any():
        errores.append("vuelos duplicados")
    if not set(df["Cancelled"].dropna().unique()) <= {0, 1}:
        errores.append("Cancelled tiene valores distintos de 0/1")
    cancel_sin_codigo = int(((df["Cancelled"] == 1) & df["CancellationCode"].isna()).sum())
    if cancel_sin_codigo:
        errores.append(f"{cancel_sin_codigo} cancelados sin código")
    faltan_clientes = [c for c in CLIENTES if c not in set(df["Reporting_Airline"])]
    if faltan_clientes:
        errores.append(f"aerolíneas cliente ausentes: {faltan_clientes}")

    fechas = pd.to_datetime(df["FlightDate"])
    resumen = {
        "periodo": f"{year}-{month:02d}",
        "filas": len(df),
        "fecha_min": fechas.min().date(),
        "fecha_max": fechas.max().date(),
        "dias": fechas.dt.date.nunique(),
        "aerolineas": df["Reporting_Airline"].nunique(),
        "aeropuertos_origen": df["Origin"].nunique(),
        "cancelados": int(df["Cancelled"].sum()),
        "pct_cancelados": round(100 * df["Cancelled"].mean(), 2),
        "filas_clientes": int(df["Reporting_Airline"].isin(CLIENTES).sum()),
        "estado": "OK" if not errores else "REVISAR",
        "observaciones": "; ".join(errores),
        "procesado": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    return resumen


def registrar(resumen: dict) -> None:
    """Agrega (o reemplaza) la fila del período en el log de ingesta."""
    nuevo = pd.DataFrame([resumen])
    if LOG_FILE.exists():
        log = pd.read_csv(LOG_FILE)
        log = log[log["periodo"] != resumen["periodo"]]
        nuevo = pd.concat([log, nuevo], ignore_index=True).sort_values("periodo")
    nuevo.to_csv(LOG_FILE, index=False)


def procesar_mes(year: int, month: int) -> dict:
    print(f"\n[{year}-{month:02d}]")
    ruta_zip = descargar(year, month)
    df = leer_zip(ruta_zip)
    resumen = validar(df, year, month)
    salida = INTERIM_DIR / f"ontime_{year}_{month:02d}.parquet"
    df.to_parquet(salida, index=False)
    registrar(resumen)
    print(f"  → {resumen['filas']:,} filas | {resumen['pct_cancelados']}% cancelados | "
          f"estado: {resumen['estado']} {resumen['observaciones']}")
    return resumen


def main(periodos=PERIODOS) -> pd.DataFrame:
    for carpeta in (RAW_DIR, INTERIM_DIR, LOG_FILE.parent):
        carpeta.mkdir(parents=True, exist_ok=True)
    resultados, fallidos = [], []
    for year, month in periodos:
        try:
            resultados.append(procesar_mes(year, month))
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            fallidos.append(f"{year}-{month:02d}")
    print("\n================ RESUMEN ================")
    print(f"Meses procesados: {len(resultados)} de {len(periodos)}")
    if fallidos:
        print(f"Meses con error (vuelve a ejecutar para reintentar): {fallidos}")
    return pd.DataFrame(resultados)


if __name__ == "__main__":
    main()
