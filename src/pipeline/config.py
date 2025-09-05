import os
from datetime import datetime
import sqlalchemy
import psycopg2
from dotenv import load_dotenv

#fecha de scraping de los datos
fecha_scraping = datetime.now().strftime("%Y-%m-%d").replace("-", "_")
# Carpeta raíz del proyecto (2 niveles arriba desde este archivo)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Subcarpetas de datos
RAW_DIR = os.path.join(ROOT_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(ROOT_DIR, "data", "processed")
MODELS_DIR = os.path.join(ROOT_DIR, "models")

# Crear carpetas si no existen
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

#variables de database para utilizar sql
load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

#Función para estandarizar variables numéricas.
def estandarizar(df):
    df_scaled = df.copy()
    num_cols = df.select_dtypes(include="number").columns
    
    df_scaled[num_cols] = (df[num_cols] - df[num_cols].mean()) / df[num_cols].std()
    
    return df_scaled

if __name__ == "__main__":
    print("ROOT_DIR:", ROOT_DIR)
    print("RAW_DIR:", RAW_DIR)
    print("PROCESSED_DIR:", PROCESSED_DIR)