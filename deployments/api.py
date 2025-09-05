from fastapi import FastAPI
import pandas as pd
import sqlalchemy
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime
from src.pipeline.config import engine
# Crear aplicación
app = FastAPI()


fecha_scraping = "2025_09_02"
df = pd.read_sql(f"SELECT * FROM ofertas_{fecha_scraping}", engine)


@app.get("/")
def home():
    return {"mensaje": "API de datos de libros 📚 funcionando!"}

@app.get("/datos")
def get_datos(limit: int = 10):
    """
    Devuelve las primeras filas del dataset.
    Se puede pasar un parámetro `limit` (default=10).
    """
    return df.head(limit).to_dict(orient="records")

@app.get("/categorias")
def get_categorias():
    """
    Devuelve todas las categorías únicas de libros.
    """
    categorias = df["categoria"].unique().tolist()
    return {"categorias": categorias}

@app.get("/buscar")
def buscar_libro(titulo: str):
    """
    Busca libros cuyo título contenga la palabra ingresada.
    """
    resultados = df[df["titulo"].str.contains(titulo, case=False, na=False)]
    return resultados.to_dict(orient="records")

# uvicorn deployments.api:app --reload

#http://127.0.0.1:8000/
#http://127.0.0.1:8000/datos?limit=5
#http://127.0.0.1:8000/categorias
#http://127.0.0.1:8000/buscar?titulo=poesía
#http://127.0.0.1:8000/docs#/default/get_datos_datos_get