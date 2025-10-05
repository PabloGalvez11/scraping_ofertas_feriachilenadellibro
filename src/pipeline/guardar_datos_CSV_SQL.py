import pandas as pd
import sqlalchemy
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime
from .config import fecha_scraping, PROCESSED_DIR, engine
import glob #Para importe masivo de archivos csv.

def guardar_en_SQL():

    #Importamos los archivos y agrupamos en una lista de dataframes
    archivos = glob.glob(os.path.join(PROCESSED_DIR, "ofertas_*.csv"))
    dfs = [pd.read_csv(archivo, sep=";", decimal=",", encoding="utf-8") for archivo in archivos]
    #Unimos todos los dataframes en uno solo.
    df = pd.concat(dfs, ignore_index=True)
    #aseguramos que todas las fecha están bien puestas
    df["fecha_extraccion"] = df["fecha_extraccion"].str.replace("_", "-", regex=False)
    #eliminamos duplicados, es decir, casos en que en dos fechas distintas se haya guardado un mismo libro en oferta y no presente cambio alguno en precio.
    df = df.drop_duplicates(subset=df.columns.difference(["fecha_extraccion"]), keep="first")

    #exportamos a un csv con el total de ofertas. La idea es ir acumulando. En caso de no poder guardar los archivos ofertas_2025_08_24,
    #entonces se debería hacer el append a total_ofertas_feriachilenadellibro
    df.to_csv(os.path.join(PROCESSED_DIR, "total_ofertas_feriachilenadellibro.csv"), index=False, sep=';', decimal=',', encoding="utf-8")
    #exportamos
    df.to_sql(f'total_ofertas_feriachilenadellibro', engine, index = False, if_exists = 'replace')

    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT COUNT(*) FROM total_ofertas_feriachilenadellibro"))
        print(result.scalar())


if __name__ == "__main__":
    csv_to_SQL()