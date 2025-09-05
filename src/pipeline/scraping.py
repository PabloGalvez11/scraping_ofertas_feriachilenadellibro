#Importamos librerías a utilizar
import pandas as pd #Para trabajo con datos y dataframes
import requests #para solicitud de web scraping
from bs4 import BeautifulSoup #para conversión a html y extracción de información concreta de la página.
import glob #Para importe masivo de archivos csv.
import time, random
import os
from datetime import datetime
import re
from .config import RAW_DIR, fecha_scraping

def scraping_libros():
    
    #headers para scraping (no manejo mucho cómo funcionan)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    

    #Identificamos la cantidad total de pestañas que presentan ofertas.
    url= 'https://feriachilenadellibro.cl/ofertas'
    response = requests.get(url, headers=headers)
    print(response.status_code) #verificamos el estado de respuesta (debe ser 200)
    soup = BeautifulSoup(response.text, features='html.parser')
    total_pestanas = int(soup.find_all(name = "a", attrs = {'class': 'page-numbers'})[-2].get_text(strip=True)) + 1
    print(f"Total de pestañas encontradas: {total_pestanas - 1}")

    pestana_inicial = int(input(f"Inserte la pestaña inicial de la extracción de información (considerar rango entre 1 y {total_pestanas - 1}): "))
    pestana_final = int(input(f"Inserte la pestaña final de la extracción de información (considerar rango desde pestana_inicial+1 y {total_pestanas - 1}): ")) + 1



    for pestana in range(pestana_inicial, min(pestana_final, total_pestanas)): #pestaña de la página de la cual extraer los datos

        #Creamos un dataframe vacío donde guardaremos los dataframe generados
        columnas = ["titulo", "categoria","macrocategoria", "disponibles", "precio_original", "precio_oferta", "autor", "editorial", "encuadernacion", "peso", "dimensiones","ano_edicion","paginas","idioma", "info_adicional", "descripcion", "link", "fecha_extraccion"]
        df = pd.DataFrame(columns=columnas)
        #Presentamos la url de la página de la librería de la cual extraeremos los datos.
        url= f'https://feriachilenadellibro.cl/ofertas/?product-page={pestana}'
        #enviamos solicitud al servidor para poder extraer datos.
        response = requests.get(url, headers=headers)
        print(response.status_code) #verificamos el estado de respuesta (debe ser 200)
        print(f"pagina {pestana}") #sirve como referencia para saber la página de la cual se está extrayendo los datos

        #utilizamos beautifulsoup para convertir el contenido extraído por la solicitud a html para el scraping.
        soup = BeautifulSoup(response.text, features='html.parser')
        #Creamos lista vacía en la que se guardarán los links correspondientes a la página a scrapear.
        product_links =[]
        #Extraemos los links de todos los productos (libros) presentes en dicha pestaña.
        links = soup.find_all(name = "div", attrs={'class': 'astra-shop-summary-wrap'})
        #Agregamos los links a la lista de links.
        for link in links:
            product_links.append(link.find(name="a")["href"])
        #Realizamos un ciclo for para cada url de cada producto presente en la lista de links, con motivo de extraer la información específica del producto.
        for url_libro in product_links:
            #extraemos la información de la página del producto específico
            response = requests.get(url_libro, headers=headers)
    #        time.sleep(random.uniform(1.5, 4.0))  # pausa aleatoria entre 1.5 y 4 segundos
            soup = BeautifulSoup(response.text, features='html.parser')
            titulo_tag = soup.find(name="h1", attrs={'class': 'product_title'})
            #Extraemos el título del libro
            if not titulo_tag:   # si no hay título, pasamos al siguiente libro
                print(f"❌ No se encontró información en {url_libro}, se omite.")
                continue
            # Si sí hay título, seguimos
            titulo = titulo_tag.get_text(strip=True)
            #Realizamos un print para tener noción del producto que se está extrayendo en el momento.
            print([titulo, url_libro])
            #extraemos datos de macrocategoria
            macrocategoria = soup.find(name="nav", attrs={'class': 'woocommerce-breadcrumb'})
            macrocategoria = macrocategoria.select("nav.woocommerce-breadcrumb a")[1].get_text(strip=True)
            #Extraemos información respecto al autor, editorial y encuadernación del libro.
            desc_tag = soup.find(name="div", attrs={'class': 'woocommerce-product-details__short-description'})
            if desc_tag and desc_tag.get_text(strip=True) != "…":
                detalles = [i.split(":", 1)[1].strip() for i in desc_tag.get_text(separator="\n", strip=True).split("\n")]
                autor, editorial, encuadernacion = detalles[0], detalles[1] if len(detalles) > 1 else None, detalles[2] if len(detalles) > 2 else None
            else:
                detalles = autor = editorial = encuadernacion = None
            #Extraemos el precio original y el precio de oferta del libro.
            precio_original = soup.find_all(name="span", attrs={'class': 'woocommerce-Price-amount amount'})[0].get_text(strip=True)
            precio_oferta = soup.find_all(name="span", attrs={'class': 'woocommerce-Price-amount amount'})[1].get_text(strip=True)
            #Extraemos la cantidad de unidades disponibles.
            stock_tag = soup.find(name="span", attrs={'class': 'stock in-stock'})
            disponibles = int(stock_tag.get_text(strip=True).split()[0]) if (stock_tag := soup.find("span", class_="stock in-stock")) else 0
            #Extraemos la categoría a la que corresponde el libro.
            categoria = soup.find(name="span", attrs={'class': 'posted_in'}).get_text(strip=True).split(":")[1]
            #Extraemos el texto de descripción del libro.
            descripcion = soup.find(name="div", attrs={'class': 'woocommerce-Tabs-panel'}).get_text(strip=False)
            #Extraemos información adicional del libro.
            info_adicional = soup.find_all(name="td", attrs={'class': 'woocommerce-product-attributes-item__value'})
            info_adicional = [td.get_text(strip=True) for td in info_adicional]
            info_ad = soup.find(name="table", attrs={'class': 'woocommerce-product-attributes shop_attributes'})

            # Inicializamos todas las llaves con None
            valores = {
                "peso": None,
                "dimensiones": None,
                "autor": None,
                "encuadernacion": None,
                "editorial": None,
                "idioma": None,
                "paginas": None,
                "ano_edicion": None
            }

            # Recorremos todas las filas de la tabla
            for tr in info_ad.find_all("tr", class_="woocommerce-product-attributes-item"):
                th = tr.find("th", class_="woocommerce-product-attributes-item__label")
                td = tr.find("td", class_="woocommerce-product-attributes-item__value")
                if th and td:
                    etiqueta = th.get_text(strip=True).lower()
                    valor = td.get_text(strip=True)
                    if "peso" in etiqueta:
                        valores["peso"] = valor
                    elif "dimensiones" in etiqueta:
                        valores["dimensiones"] = valor
                    elif "autor" in etiqueta:
                        valores["autor"] = valor
                    elif "encuadernación" in etiqueta or "encuadernacion" in etiqueta:
                        valores["encuadernacion"] = valor
                    elif "editorial" in etiqueta:
                        valores["editorial"] = valor
                    elif "idioma" in etiqueta:
                        valores["idioma"] = valor
                    elif "páginas" in etiqueta or "paginas" in etiqueta:
                        valores["paginas"] = valor
                    elif "año" in etiqueta:
                        valores["ano_edicion"] = valor
            #Asignamos los valores de información adicional.
            peso = valores["peso"]
            dimensiones = valores["dimensiones"]
            ano_edicion = valores["ano_edicion"]
            paginas = valores["paginas"]
            idioma = valores["idioma"]
            #Agregamos todas la información extraída del libro como una fila para el dataframe vacío.
            fila = pd.DataFrame([{
                "titulo": titulo,
                "categoria": categoria,
                "macrocategoria": macrocategoria,
                "disponibles": disponibles,
                "precio_original": precio_original,
                "precio_oferta": precio_oferta,
                "autor": autor,
                "editorial": editorial,
                "encuadernacion": encuadernacion,
                "peso": peso,
                "dimensiones": dimensiones,
                "ano_edicion": ano_edicion,
                "paginas": paginas,
                "idioma": idioma,
                "info_adicional": info_adicional,
                "descripcion": descripcion,
                "link": url_libro,
                "fecha_extraccion": fecha_scraping
            }])
            df = pd.concat([df, fila], ignore_index=True)
        #Exportamos el csv de la pagina especificada
        if df.empty:
            print(f"No se presentan datos en la pestaña {pestana}, por lo tanto se omite.")
            continue
        df.to_csv(os.path.join(RAW_DIR, f"ofertas_{fecha_scraping}_raw_pag_{pestana}.csv"), index=False, encoding="utf-8")



    #Importamos los archivos y agrupamos en una lista de dataframes
    archivos = glob.glob(os.path.join(RAW_DIR, f"ofertas_{fecha_scraping}_raw_pag_*.csv"))
    dfs = [pd.read_csv(archivo) for archivo in archivos]
    #Unimos todos los dataframes en uno solo.
    df = pd.concat(dfs, ignore_index=True)

    #exportamos el csv
    df.to_csv(os.path.join(RAW_DIR, f"ofertas_{fecha_scraping}_raw.csv"), index=False, encoding="utf-8")

    for archivo in archivos:
        os.remove(archivo)
        #print(f"Eliminado: {archivo}")

# Bloque de ejecución directa
if __name__ == "__main__":
    # Ejecutar solo si corremos python scraping.py
    scraping_libros()