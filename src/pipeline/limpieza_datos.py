#Importamos librerías a utilizar
import pandas as pd #Para trabajo con datos y dataframes
import requests #para solicitud de web scraping
from bs4 import BeautifulSoup #para conversión a html y extracción de información concreta de la página.
import glob #Para importe masivo de archivos csv.
from unidecode import unidecode #para eliminación de tildes en observaciones.
import numpy as np
from datetime import datetime
import re
import os
from .config import RAW_DIR, fecha_scraping, PROCESSED_DIR




def limpieza_datos():

    #Importamos la data
    df = pd.read_csv(os.path.join(RAW_DIR, f"ofertas_{fecha_scraping}_raw.csv"), encoding="utf-8")

    #Limpiamos los valores de precio original y precio de oferta para que queden en formato numérico de número flotante.
    df["precio_original"] = df["precio_original"].str.replace("$", "", regex=False).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
    df["precio_oferta"] = df["precio_oferta"].str.replace("$", "", regex=False).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
    #Creamos una variable asociada al porcentaje de descuento que fue aplicado.
    porcentaje_descuento = (1 - (df["precio_oferta"] / df["precio_original"])).round(2)
    idx = df.columns.get_loc("precio_oferta")
    df.insert(idx + 1, "porcentaje_descuento", porcentaje_descuento)
    #Eliminamos registros con porcentaje de descuento negativo, ya que en realidad estos no están con descuento activo al visitar el link.
    df = df[df["porcentaje_descuento"] > 0]

    #Limpiamos los valores de la variable "peso" para conservarlo como número flotante en kg.
    df["peso"] = df["peso"].str.replace(" kg", "", regex=False).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
    df = df.rename(columns={"peso": "peso_kg"})

    #Separamos la variable dimensiones en largo, ancho y grosor del libro.
    # función auxiliar para limpiar y corregir
    def limpiar_valor(i):
        v = float(i.replace(",", ".").replace("cm", "").strip())
        if 100 <= v <= 999:  # si tiene tres cifras
            v *= 0.1
        return v

    # aplicar la transformación
    nuevas = df["dimensiones"].apply(
        lambda x: pd.Series(
            sorted([limpiar_valor(i) for i in x.split("×")], reverse=True)
        )
    )

    # insertar las nuevas columnas después de "dimensiones"
    idx = df.columns.get_loc("dimensiones")
    df.insert(idx + 1, "largo", nuevas[0])
    df.insert(idx + 2, "ancho", nuevas[1])
    df.insert(idx + 3, "grosor", nuevas[2])

    #Estandarizamos los textos de las variables de tipo string. Eliminamos tildes y transformamos los textos a minúsculas.
    df["titulo"] = df["titulo"].astype(str).apply(lambda x: unidecode(x).lower())
    df["categoria"] = df["categoria"].astype(str).apply(lambda x: unidecode(x).lower())
    df["macrocategoria"] = df["macrocategoria"].astype(str).apply(lambda x: unidecode(x).lower())
    df["autor"] = df["autor"].astype(str).apply(lambda x: unidecode(x).lower())
    df["editorial"] = df["editorial"].astype(str).apply(lambda x: unidecode(x).lower())
    df["encuadernacion"] = df["encuadernacion"].astype(str).apply(lambda x: unidecode(x).lower())

    #descripcion_limpia = re.sub(r'(?<![A-Z])(?=[A-Z])', ' ', descripcion).strip()
    #descripcion_limpia = re.sub(r'\s+', ' ', descripcion_limpia)

    def limpiar_descripcion(texto):
        if pd.isna(texto):  # Maneja valores NaN
            return texto

        # 1️⃣ Insertar espacio antes de mayúscula que sigue a minúscula o puntuación
        texto_limpia = re.sub(r'(?<![A-Z])(?=[A-Z])', ' ', texto).strip()

        # 2️⃣ Quitar espacios después de signos iniciales ¿ y ¡
        texto_limpia = re.sub(r'([¿¡])\s+', r'\1', texto_limpia)

        # 3️⃣ Normalizar espacios
        texto_limpia = re.sub(r'\s+', ' ', texto_limpia)

        return texto_limpia

    df['descripcion'] = df['descripcion'].apply(limpiar_descripcion)


    #creamos la variable volumen para reemplazar a las de dimensiones, ya que pueden ser muy correlacionadas.
    df["volumen"] = df["largo"] * df["ancho"] * df["grosor"] 


    print(df["idioma"].value_counts())
    #dado que hay tan poca variabilidad en cuanto a la variable idioma, se opta por eliminar la variable, ya que no es de utilidad.
    #Por otra parte, dado que ya separamos las dimensiones en tres variables distintas, procedemos a eliminar dicha variable, ya que es redundante.
    df = df.drop(columns=["idioma","dimensiones", "info_adicional"])

    #Eliminamos registros cuyos valores para las variables ano_edicion, paginas sean NaN (None).
    #Esto debido a que dichas variables se consideran de gran relevancia para un análisis.
    df = df.dropna(subset=['ano_edicion', 'paginas']).reset_index(drop=True) #dropeamos alrededor de 80 observaciones.

    #Se opta por no eliminar ninguna columna en este jupyter notebook, sino que será en PowerBI.

    #Dependiendo del foco que se tenga, las variables asociadas al título, autor, editorial, descripcion, link pueden adoptar mayor o menor importancia para un análisis.

    #Verificamos la presencia de valores NaN dentro del dataframe
    print(df.isnull().any())
    print(df["grosor"].isna().value_counts())
    #Sólo la variable "grosor" presenta valores NaN.
    #Debido a que aún dicha variable no se considera de gran relevancia y además sólo presenta 3 registros faltantes, se opta por conservarlos.

    #Se opta por eliminarlos, más fácil
    df = df.dropna(subset=['grosor'])
    print(df["grosor"].isna().value_counts())


    #Reasignamos la macrocategoría de literatura debido a su amplia variedad de títulos.
    frecuencias = df[df["macrocategoria"]=="literatura"]["categoria"].value_counts()
    #Utilizaremos la respectiva categoría a los títulos cuya categoría tenga una frecuencai mayor o igual a 10. 
    #Por otra parte reasignaremos como "otra literatura" a los que tengan una menor frecuencia
    categorias_frecuentes = frecuencias[frecuencias >= 10].index
    df.loc[(df["macrocategoria"] == "literatura") & (df["categoria"].isin(categorias_frecuentes)),"macrocategoria"] = df["categoria"]
    df.loc[(df["macrocategoria"] == "literatura") & (~df["categoria"].isin(categorias_frecuentes)), "macrocategoria"] = "otra literatura"

    #Con el siguiente código, identificaremos los títulos de literaturas cuyas categorías fueron modificadas y se le agregará el prefijo "literatura ".
    #En caso de ya presentarlo, no se le agrega para no redundar. Se le agrega srt.startswith para identificar los títulos que ya presentan el prefijo.
    mask = df["macrocategoria"].isin(categorias_frecuentes)
    df.loc[mask, "macrocategoria"] = "literatura " + df.loc[mask, "macrocategoria"].where(
        df.loc[mask, "macrocategoria"].str.lower().str.startswith("literatura"),
        ""
    ) + df.loc[mask, "macrocategoria"]




    #Exportamos el dataframe 
    df.to_csv(os.path.join(PROCESSED_DIR, f"ofertas_{fecha_scraping}.csv"), index=False, sep=';', decimal=',', encoding="utf-8")



if __name__ == "__main__":
    limpieza_datos()