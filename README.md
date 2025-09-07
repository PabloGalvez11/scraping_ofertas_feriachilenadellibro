# 📚 Proyecto de Web Scraping y análisis de datos - ofertas de la página de la librería Feria Chilena del libro ("https://feriachilenadellibro.cl") 📚

Este proyecto consiste en la aplicación en conjunto de diversas técnicas aprendidas para la elaboración de un pipeline a partir de datos reales extraídos de la página web de la librería Feria Chilena del Libro, concretamente de las ofertas ofrecidas vía internet.

El proyecto tiene por objetivo abarcar y practicar el uso de diversas habilidades que puedan realizarse con sólo poseer un nicho de datos. 

## Estructura del proyecto

### Carpetas del proyecto

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
- **guardar_en_SQL.py**: Contiene el código para el guardado de datasets dentro de la base de datos.
- **flow.py**: Contiene el flujo para el funcionamiento del pipeline.
- **limpieza_datos.py**: Contiene el proceso de limpieza de datos de los datos extraídos por medio de web scraping.
- **modelo_descuento.py**: Contiene el proceso para el entrenamiento, predicción y exportación del modelo relacionado a predecir el porcentaje de descuento de un libro.
- **modelo_precio_oferta.py**: Contiene el proceso para el entrenamiento, predicción y exportación del modelo relacionado a predecir el precio de oferta de un libro.
- **modelo_precio_original.py**: Contiene el proceso para el entrenamiento, predicción y exportación del modelo relacionado a predecir el precio original de un libro.
- **scraping.py**: Contiene el proceso de extracción de datos mediante web scraping.

### Archivos adicionales
- **.env**: Se utiliza para guardar las credenciales de la base de datos.
- **.env.example**: Se utiliza para que otras personas puedan realizar el proceso sin utilizar mis mismas credenciales de la base de datos.
- **requirements.txt**: Contiene todas las librerías utilizadas dentro del proyecto, algunas con sus respectivas versiones.

## Metodología

Se contemplan los siguientes pasos generales dentro del pipeline para la creación de un flujo para el proceso de extracción, limpieza, análisis predictivo, NLP y guardado de datos:

---

### 0. Definir variables y directorios a utilizar

Se realizó dentro de `config.py`. Este archivo contiene variables y funciones definidas para proveer a los demás archivos, tales como la fecha de extracción de datos (fecha de hoy), detalles de la base de datos local, directorio de carpetas y función para estandarización. Si bien, no se puede considerar un paso como tal, es crucial su inclusión previa a los otros pasos.

###  1. Web Scraping para extracción de datos

Se realizó dentro de `scraping.py`, principalmente con uso de la librería `BeautifulSoup`. El proceso consiste en:
- Identificar la cantidad de pestañas dentro de la sección de ofertas, para luego solicitar al usuario entre qué pestañas realizar la extracción 
- Ingresar uno por uno al link de cada libro dentro de la sección de ofertas, para luego extraer información más detallada acerca del libro ofertado.
- Cada página de la sección de ofertas se guarda como archivo .csv para luego ser eliminados y unidos en uno solo, con nombre respectivo a la fecha de extracción. Dicho proceso toma alrededor de 2 horas.

### 2. Limpieza de los datos extraídos

Se realizó dentro de `limpieza_datos.py`, principalmente con uso de las librerías `pandas` y `numpy`. El proceso consiste en:

- Limpieza de variables numéricas y categóricas. 
- Creación de variables, eliminación de valores irregulares, reasignación de categorías.
- Limpieza de variable de texto asociada a la descripción del libro para su posterior uso en NLP.

### 3. Guardado de datos dentro de una base de datos local PostgreSQL

Se realizó dentro de `guardar_en_SQL.py`, principalmente con uso de las librerías `pandas`, `sqlalchemy` y `psycopg2`. El proceso consiste en utilizar la variable engine definida dentro de `config.py` correspondiente a la dirección de la base de datos creada en PostgreSQL.

### 4. Análisis predictivo de variables asociadas a un libro.

Se realizaron de manera paralela tres modelos predictivos para variables asociadas a los libros, separadas en tres distintos archivos. Dentro de cada archivo se ajustaron los datos acorde a la variable objetivo, para luego entrenar, guardar y testear los modelos. Los modelos entrenados fueron guardados dentro de la carpeta models. Los modelos son los siguientes:

- **Precio original**: Dentro del archivo `modelo_precio_original.py`, con objetivo de predecir el precio original de un libro, se ajustó un modelo de regresión lineal.
- **Precio de oferta**: Dentro del archivo `modelo_precio_oferta.py`, con objetivo de predecir el precio de oferta de un libro, se ajustó un modelo de regresión lineal.
- **Descuento**: Dentro del archivo `modelo_descuento.py`, con objetivo de predecir el porcentaje de descuento de un libro, separado en rangos de categorías, se ajustó un modelo de regresión multinomial ordinal, con aplicación de técnicas de remuestreo como SMOTE. Para este caso en particular, las predicciones no suelen ser muy precisas.

### 5. Uso de técnicas de Procesamiento del Lenguaje Natural (NLP)

Aún en construcción y evaluando si es posible agregarlo al pipeline.

### 6. Creación de flujo de datos

Se realizó dentro de `flow.py`, utilizando la librería `prefect` para ello.
Dentro del archivo se definieron los pasos "task" y se juntaron dentro del flujo "flow". Siguiendo un orden de extracción, limpieza, guardado y finalmente modelamiento de los datos.


## Apartados adicionales

Se incluirán los siguintes apartados a ser practicados, que bien pueden incorporarse después del paso de guardado de datos:
- Creación de API mediante FastAPI de manera local.
- Análisis descriptivo con visualización de gráficas por medio de PowerBI.
- Guardado en repositorio de GitHub.