import pandas as pd
import sqlalchemy
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime
from .config import fecha_scraping, PROCESSED_DIR, engine

def csv_to_SQL():

    df = pd.read_csv(os.path.join(PROCESSED_DIR, f'ofertas_{fecha_scraping}.csv'), sep=";", decimal=",", encoding="utf-8")

    df.to_sql(f'ofertas_{fecha_scraping}', engine, index = False, if_exists = 'replace')

    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(f"SELECT COUNT(*) FROM ofertas_{fecha_scraping}"))
        print(result.scalar())


if __name__ == "__main__":
    csv_to_SQL()