# 📚 Proyecto de Web Scraping y análisis de datos - ofertas de la página de la librería Feria Chilena del libro ("https://feriachilenadellibro.cl") 📚

Este proyecto consiste en la aplicación en conjunto de diversas técnicas aprendidas para la elaboración de un pipeline a partir de datos reales extraídos de la página web de la librería Feria Chilena del Libro, concretamente de las ofertas ofrecidas vía internet.

El proyecto tiene por objetivo abarcar y practicar el uso de diversas habilidades que puedan realizarse con sólo poseer un nicho de datos. 

---

## Estructura del proyecto

---

Se contemplan los siguientes pasos generales:

- Extracción de datos mediante uso de Web Scraping
- Limpieza de los datos extraídos para su posterior análisis.
- Guardado de datos limpios dentro de una base de datos local por medio de PostgreSQL.
- Análisis predictivo de tres distintas variables provenientes de la base de datos.
- Uso de técnicas de Procesamiento del Lenguaje Natural (NLP) a partir de descripciones de libros.

Dichos pasos anteriores servirán para la creación de un flujo para el proceso de extracción, limpieza, análisis predictivo, NLP y guardado.


Además, se incluirán los siguintes apartados a ser practicados:
- Creación de API mediante FastAPI de manera local.
- Análisis descriptivo con visualización de gráficas por medio de PowerBI.
- Guardado en repositorio de GitHub.


## Carpetas del proyecto

- **data/raw** : Contiene los datos obtenidos mediante web scraping.
- **data/processed** : Contiene los datos de raw luego de haberles realizado.
- **deployments**: Contiene el código para la creación de una web API.
- **models**: Contiene los tres tipos de modelos separados en carpetas según la variable objetivo.
- **notebooks**: Contiene los códigos "prototipo" de los pasos previos a la estructuración en archivos .py.
- **paletas de colores**: Contiene paletas de colores para ser utilizadas en PowerBI.
- **queries**: Contiene las queries que se realizaron para la creación de la base de datos en PostgreSQL.
- **src/pipeline**: Contiene los archivos .py utilizados para la elaboración del pipeline.
- **words**: Contiene documentos de texto word con códigos para la creación de medidas y columnas DAX, además de preguntas para responder con gráficas de PowerBI.



### Archivos dentro de src/pipeline
- **__init__.py**: Se utiliza para asignar la carpeta de pipeline como un paquete.
- **config.py**: Contiene variables y funciones definidas para proveer a los demás archivos.
- **csv_to_SQL**: Contiene el código para el guardado de datasets dentro de la base de datos.
- **flow.py**: Contiene el flujo para el funcionamiento del pipeline.
- **limpieza_datos.py**: Contiene el proceso de limpieza de datos de los datos extraídos por medio de web scraping.
- **modelo_descuento.py**: Contiene el proceso para el entrenamiento, predicción y exportación del modelo relacionado a predecir el porcentaje de descuento de un libro.
- **modelo_precio_oferta.py**: Contiene el proceso para el entrenamiento, predicción y exportación del modelo relacionado a predecir el precio de oferta de un libro.
- **modelo_precio_original.py**: Contiene el proceso para el entrenamiento, predicción y exportación del modelo relacionado a predecir el precio original de un libro.
- **scraping.py**: Contiene el proceso de extracción de datos mediante web scraping.

## Archivos adicionales
- **.env**: Se utiliza para guardar las credenciales de la base de datos.
- **.env.example**: Se utiliza para que otras personas puedan realizar el proceso sin utilizar mis mismas credenciales de la base de datos.
- **requirements.txt**: Contiene todas las librerías utilizadas dentro del proyecto, algunas con sus respectivas versiones.

