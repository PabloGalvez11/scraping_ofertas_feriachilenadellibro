from prefect import flow, task
from .scraping import scraping_libros
from .limpieza_datos import limpieza_datos
from .csv_to_SQL import csv_to_SQL
from .modelo_precio_original import modelo_precio_original
from .modelo_precio_oferta import modelo_precio_oferta
from .modelo_descuento import modelo_descuento

@task(persist_result=False, cache_result_in_memory=False)
def scraping_task():
    return scraping_libros()

@task(persist_result=False, cache_result_in_memory=False)
def limpieza_datos_task():
    return limpieza_datos()

@task(persist_result=False, cache_result_in_memory=False)
def guardar_en_SQL_task():
    return csv_to_SQL()

@task(persist_result=False, cache_result_in_memory=False)
def modelo_precio_original_task():
    return modelo_precio_original()

@task(persist_result=False, cache_result_in_memory=False)
def modelo_precio_oferta_task():
    return modelo_precio_oferta()

@task(persist_result=False, cache_result_in_memory=False)
def modelo_descuento_task():
    return modelo_descuento()

@flow
def mi_flow():
    scraping_task()
    print("Scraping completo")
    limpieza_datos_task()
    print("Limpieza de datos completa")
    guardar_en_SQL_task()
    print("Datos guardados en SQL")
    modelo_precio_original_task()
    modelo_precio_oferta_task()
    print("Modelos de precios entrenados y con predicciones hechas")
    modelo_descuento_task()
    print("Modelo de descuento entrenado y con predicciones hechas")
    print("Flow completado")

if __name__ == "__main__":
    mi_flow()

#python -m src.pipeline.flow

















