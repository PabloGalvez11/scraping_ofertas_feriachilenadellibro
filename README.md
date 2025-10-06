# 📚 Proyecto de Web Scraping y análisis de datos - ofertas de la página de la librería Feria Chilena del libro ("https://feriachilenadellibro.cl") 📚

Este proyecto consiste en la aplicación en conjunto de diversas técnicas aprendidas para la elaboración de un pipeline a partir de datos reales extraídos de la página web de la librería Feria Chilena del Libro, concretamente de las ofertas ofrecidas vía internet.

El proyecto tiene por objetivo abarcar y practicar el uso de diversas habilidades que puedan realizarse con sólo poseer un nicho de datos. Dado que sólo se apunta a extraer datos de ofertas, no se espera una gran base de datos, como mucho una tabla de datos.

Se evaluó dividir en README's según carpeta, pero se optó por mantener toda la explicación de la información en un sólo archivo, lo que puede resultar en un documento muy abrumador.

De antemano pido disculpas si la explicación de cada sección no es muy clara. Se tiene en cuenta siempre la posibilidad de mejora.

## Estructura del proyecto

### Carpetas del proyecto

- **data/raw** : Contiene los datos obtenidos mediante web scraping.
- **data/processed** : Contiene los datos de raw luego de haberles realizado.
- **deployments**: Contiene el código para la creación de una web API.
- **models**: Contiene los tres tipos de modelos separados en carpetas según la variable objetivo. Se van acumulando según el flujo que se realiza. La idea es el entrenamiento de un nuevo modelo utilizando el total de registros según la fecha de ejecución, por lo que se espera que un modelo antiguo haya sido entrenado con menos registros que uno más reciente, ya que el más reciente utiliza los registro extraídos en fechas pasadas y además incluye los de la extracción más reciente.
- **notebooks**: Contiene los códigos "prototipo" de los pasos previos a la estructuración en archivos .py.
- **queries**: Contiene las queries que se realizaron para la creación de la base de datos en PostgreSQL.
- **src/pipeline**: Contiene los archivos .py utilizados para la elaboración del pipeline.
- **PowerBI**: Contiene documentos de texto word con códigos para la creación de medidas y columnas DAX, además de preguntas para responder con gráficas de PowerBI, paletas de colores descargadas que podrían ser usadas en un dashboard de PowerBI y finalmente el archivo que contiene el dashboard interactivo de PowerBI creado `visualizacion.pbix` para la visualización gráfica de los datos, junto a su versión en pdf para un formato general, aunque no interactivo `visualizacion.pdf`.



### Archivos dentro de src/pipeline
- **__init__.py**: Se utiliza para asignar la carpeta de pipeline como un paquete.
- **config.py**: Contiene variables y funciones definidas para proveer a los demás archivos.
- **guardar_datos_CSV_SQL.py**: Contiene el código para el guardado de datasets dentro de la base de datos.
- **flow.py**: Contiene el flujo para el funcionamiento del pipeline.
- **limpieza_datos.py**: Contiene el proceso de limpieza de datos de los datos extraídos por medio de web scraping.
- **modelo_descuento.py**: Contiene el proceso para el entrenamiento, predicción y exportación del modelo relacionado a predecir el porcentaje de descuento de un libro.
- **modelo_precio_oferta.py**: Contiene el proceso para el entrenamiento, predicción y exportación del modelo relacionado a predecir el precio de oferta de un libro.
- **modelo_precio_original.py**: Contiene el proceso para el entrenamiento, predicción y exportación del modelo relacionado a predecir el precio original de un libro.
- **NLP_token_stem_lemma.py**: Contiene el proceso de aplicación de técnicas de procesamiento del lenguaje natural (NLP) como tokenización, stemming, lemma, creación y ajuste de modelos para identificar la macrocategoría a la que pertenece un libro según su descripción.
- **scraping.py**: Contiene el proceso de extracción de datos mediante web scraping.

### Archivos adicionales
- **.env**: Se utiliza para guardar las credenciales de la base de datos.
- **.env.example**: Se utiliza para que otras personas puedan realizar el proceso sin utilizar mis mismas credenciales de la base de datos.
- **requirements.txt**: Contiene todas las librerías utilizadas dentro del proyecto, algunas con sus respectivas versiones.

## Metodología

Se contemplan los siguientes pasos generales dentro del pipeline para la creación de un flujo para el proceso de extracción, limpieza, análisis predictivo con machine learning, NLP y proceso de guardado de datos en un archivo csv consolidado y una base de datos PostgreSQL.

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

Se realizó dentro de `guardar_datos_CSV_SQL.py`, principalmente con uso de las librerías `pandas`, `sqlalchemy` y `psycopg2`. El proceso consiste en utilizar la variable engine definida dentro de `config.py` correspondiente a la dirección de la base de datos creada en PostgreSQL.

### 4. Análisis predictivo de variables asociadas a un libro.

Se realizaron de manera paralela tres modelos predictivos para variables asociadas a los libros, separadas en tres distintos archivos. Dentro de cada archivo se ajustaron los datos acorde a la variable objetivo, para luego entrenar, guardar y testear los modelos. Los modelos entrenados fueron guardados dentro de la carpeta models. Los modelos son los siguientes:

- **Precio original**: Dentro del archivo `modelo_precio_original.py`, con objetivo de predecir el precio original de un libro, se ajustó un modelo de regresión lineal.
- **Precio de oferta**: Dentro del archivo `modelo_precio_oferta.py`, con objetivo de predecir el precio de oferta de un libro, se ajustó un modelo de regresión lineal.
- **Descuento**: Dentro del archivo `modelo_descuento.py`, con objetivo de predecir el porcentaje de descuento de un libro, separado en rangos de categorías, se ajustó un modelo de regresión multinomial ordinal, con aplicación de técnicas de remuestreo como SMOTE. Para este caso en particular, las predicciones no suelen ser muy precisas.

### 5. Uso de técnicas de Procesamiento del Lenguaje Natural (NLP)

Aún en construcción y evaluando si es posible agregarlo al pipeline.
Se realizó dentro de `NLP_token_stem_lemma.py`, utilizando librerías para la aplicación de técnicas de NLP como tokenización, stemming, lemmatization. Se ajustaron y realizaron predicciones con los tres modelos dichos, con objetivo de clasificar la macrocategoría a la que pertenece un libro según su descripción. Se ajustó un modelo de regresión multinomial para ello. Se obtuvo la accuracy de cada modelo para poder ser comparados. Para este caso se decidió no exportar los modelos a un archivo .joblib. Por otra parte, dentro del notebook `Paso_6_NLP_token_stem_lemma_tfidf.ipynb` también se agregó el uso del método TF-IDF para crear una recomendación de libros según macrocategoría, categoría, autor de un libro seleccionado, sin embargo, este apartado no será agregado dentro de los pasos.

### 6. Creación de flujo de datos

Se realizó dentro de `flow.py`, utilizando la librería `prefect` para ello.
Dentro del archivo se definieron los pasos "task" y se juntaron dentro del flujo "flow". Siguiendo un orden de extracción, limpieza, guardado y finalmente modelamiento de los datos.

### 7. Análisis descriptivo con visualización de gráficas por medio de PowerBI

Se realizó dentro del archivo `visualizacion.pbix`, con objetivo de realizar una visualización gráfica de los datos extraídos e ingresados a la base de datos PostgreSQL, por lo que el dashboard se alimenta de dicha base de datos, no de archivos csv. Se considera bastante simple y a lavez sobrecargada, con muchos puntos a mejorar, sin embargo, la idea es mostrar una parte de mi manejo de dicha herramienta, considerando la escasa experiencia laboral en trabajos de este estilo. Por otra parte, se puede ver de manera general el dashboard mediante el archivo `visualizacion.pdf`, pero en este no es posible interactuar con los paneles.

---
## Apartados adicionales

Se evaluará incluir los siguintes apartados a ser practicados, que bien pueden incorporarse después del paso de guardado de datos:
- Creación de API mediante FastAPI de manera local.

## Cierre

A pesar de ser algo rudimentario, este proyecto subido a GitHub me permitió aplicar y aprender técnicas para la creación de un pipeline de datos bastante útil que automatiza todo un proceso desde la extracción hasta el guardado de datos, así como la aplicación y exportación de modelos de predicción dentro de un entorno local, todo de manera autodidacta, junto a videos de youtube, consultas a ChatGPT y algo de criterio arbitrario.

Por una parte, al ser un objetivo autoimpuesto, me permitió aprender sobre la creación de un flujo de datos, web scraping, guardado en SQL, uso de repositorios de GitHub, procesamiento del lenguaje natural y visualización de datos en PowerBI.

Con la presencia de un objetivo claro como este proyecto, tengo una vía clara para la búsqueda de soluciones. 
La desventaja es que al ser un proyecto independiente, no me impuse un horario fijo, por lo que el ritmo de trabajo fue intermitente. De haber sido riguroso en ese sentido, probablemente me habría tomado un mes aproximadamente y no dos.

Se deja abierta la posibilidad de utilizar cosas como contenedores, docker, entre otros, sin embargo, sería una aplicación adicional.

Para finalizar, es de mi agrado decir que me encuentro satisfecho con lo aprendido en este proyecto, ya que gran parte de lo aplicado no tendría oportunidad de aprenderlo en la universidad y posiblemente en algún cargo hubiese tardado en llegar al punto de tener que necesitarlo, por lo que valoro aún más el conocimiento adquirido de manera independiente en este proyecto.

Entre otros objetivos, se encuentra el aprender más sobre APIs, Selenium, embeddings, LLM, contenedores, despliegue de modelos, ingeniería de datos en general, aplicación de ciencia de datos en finanzas, así como incorporarme a aprender más sobre inversiones, análisis de riesgo y trading.

Sin más que agregar, se pone fin al proyecto y pido disculpas si ocasioné problemas a la página de la Feria Chilena del Libro, ya que mi web scraping fue muy descarado, sin tiempos de pausa.