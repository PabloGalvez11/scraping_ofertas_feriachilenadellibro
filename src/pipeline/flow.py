from prefect import flow, task
from .scraping import scraping_libros
from .limpieza_datos import limpieza_datos
from .guardar_en_SQL import guardar_datos_CSV_SQL
from .modelo_precio_original import modelo_precio_original
from .modelo_precio_oferta import modelo_precio_oferta
from .modelo_descuento import modelo_descuento
from .NLP_token_stem_lemma import NLP_token_stem_lemma

@task(persist_result=False, cache_result_in_memory=False)
def scraping_task():
    return scraping_libros()

@task(persist_result=False, cache_result_in_memory=False)
def limpieza_datos_task():
    return limpieza_datos()

@task(persist_result=False, cache_result_in_memory=False)
def guardar_datos_CSV_SQL_task():
    return guardar_datos_CSV_SQL()

@task(persist_result=False, cache_result_in_memory=False)
def modelo_precio_original_task():
    return modelo_precio_original()

@task(persist_result=False, cache_result_in_memory=False)
def modelo_precio_oferta_task():
    return modelo_precio_oferta()

@task(persist_result=False, cache_result_in_memory=False)
def modelo_descuento_task():
    return modelo_descuento()

@task(persist_result=False, cache_result_in_memory=False)
def NLP_token_stem_lemma_task():
    return NLP_token_stem_lemma()


@flow
def mi_flow():
    scraping_task()
    print("Scraping completo")
    limpieza_datos_task()
    print("Limpieza de datos completa")
    guardar_datos_CSV_SQL_task()
    print("Datos guardados en SQL")
    modelo_precio_original_task()
    modelo_precio_oferta_task()
    print("Modelos de precios entrenados y con predicciones hechas")
    modelo_descuento_task()
    print("Modelo de descuento entrenado y con predicciones hechas")
    NLP_token_stem_lemma_task()
    print("Modelos NLP de identificación de macrocategoría según descripción hechos")
    print("Flow completado")

if __name__ == "__main__":
    mi_flow()

#python -m src.pipeline.flow

















