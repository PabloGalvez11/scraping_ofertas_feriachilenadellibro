#Importamos librerías
import pandas as pd
import numpy as np

import os
from sklearn.model_selection import train_test_split

#Importamos librerías para el caso de tokenización
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
#Importamos librerías que serán utilizadas para el stemming
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
#Importamos la librería requerida para la lematización
import spacy

from .config import RAW_DIR, fecha_scraping, PROCESSED_DIR

def NLP_token_stem_lemma():

    #Importamos los datos
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "total_ofertas_feriachilenadellibro.csv"), sep=";", decimal=",", encoding="utf-8") 
    #Identificamos duplicados y los eliminamos, ya que sería redundante tener dos registros idénticos cuya única diferencia fue cuándo fue hecho el scraping.
    print(df.duplicated(subset=df.columns.difference(["fecha_extraccion"]), keep=False).value_counts())
    df = df.drop_duplicates(subset=df.columns.difference(["fecha_extraccion"]), keep="first")
    #Conservamos sólo las variables que serán utilizadas para la implementación de técnicas NLP.
    df = df[["titulo","categoria","macrocategoria","autor","descripcion"]]
    #Asignamos como minúsculas todas las letras de descripción
    df["descripcion"] = df["descripcion"].str.lower()
    #Eliminamos en "descripcion" todos los trozos de texto que incluyan explícitamente el nombre del título, ya que sino no tendría sentido para casos como el método TF-IDF
    df["descripcion"] = df.apply(lambda row: row["descripcion"][len(row["titulo"])+1:].strip(), axis=1)
    #Eliminamos espacios en los extremos.
    df["descripcion"] = df["descripcion"].str.strip()


    #Asignamos la variable dependiente e independiente
    X = df["descripcion"]
    y = df["macrocategoria"]

    #############Apartado de TOKENIZACION

    #Separamos conjunto de entrenamiento y test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #Vectorizamos la variable dependiente. Como la variable son filas de texto, entonces tiene dimensión de 3000 observaciones con cada una 35941 palabras distintas.
    vectorizer = CountVectorizer()
    X_train_transformed = vectorizer.fit_transform(X_train)
    X_test_transformed = vectorizer.transform(X_test)
    #Creamos y ajustamos un modelo multinomial con el cual se predicirá la macrocategoría según el método de tokenización.
    model = MultinomialNB()
    model.fit(X_train_transformed, y_train)
    y_pred = model.predict(X_test_transformed)
    #Vemos que se logra predecir correctamente un 27.8% del conjunto de prueba
    print("Accuracy tokenización:", metrics.accuracy_score(y_test, y_pred))

    ############# Apartado de STEMMING

    #Descargamos conjuntos de palabras
    nltk.download('punkt') #para modelos
    nltk.download('stopwords') #palabras como el la los... etc.
    nltk.download('punkt_tab') #para modelos, pero es el más reciente
    stemmer = SnowballStemmer('spanish') #creamos el stemmer y especificamos el idioma.

    #creamos la función para realizar la tokenización y stemming. Además, se le agrega el ignorar las stopwords para no tener un montón de palabras que no aportan información en el fondo.
    def tokenize_and_stem(text):
        tokens = word_tokenize(text.lower())
        #hacemos el stemming
        #stems = [stemmer.stem(token) for token in tokens if token.isalpha()]
        stop_words = set(stopwords.words('spanish'))
        stems = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]
        #los unimos para la nueva frase stemmeada
        return ' '.join(stems)

    #Creamos una columna con los datos stemmeados
    df["descripcion_stemmer"] = df["descripcion"].apply(tokenize_and_stem)

    #Asignamos como variable independiente a la nueva columna creada
    X = df["descripcion_stemmer"]
    y = df["macrocategoria"]

    #Separamos en conjunto de entrenamiento y testeo y vectorizamos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    vectorizer = CountVectorizer()
    X_train_transformed = vectorizer.fit_transform(X_train)
    X_test_transformed = vectorizer.transform(X_test)
    X_train_transformed

    #Creamos y ajustamos el modelo
    model = MultinomialNB()
    model.fit(X_train_transformed, y_train)
    y_pred = model.predict(X_test_transformed)
    #Vemos que se logra predecir correctamente un 36.7% del conjunto de prueba, por lo que mejora
    print("Accuracy Stemming:", metrics.accuracy_score(y_test, y_pred)) #mejora

    ############# Apartado de LEMMATIZATION


    #se descarga el modelo para identificar los datos en español
    nlp = spacy.load('es_core_news_sm')

    #Creamos la función de tokenización que aplica lemmatization
    def lemmatize_text(text):
        doc = nlp(text.lower())
        lemmas = [token.lemma_ for token in doc if token.is_alpha]
        return ' '.join(lemmas)
    #Creamos una columna con los datos lemmatizados
    df["descripcion_lemma"] = df["descripcion"].apply(lemmatize_text)

    #Asignamos como variable independiente a la nueva columna creada
    X = df["descripcion_lemma"]
    y = df["macrocategoria"]

    #Separamos en conjunto de entrenamiento y testeo y vectorizamos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    vectorizer = CountVectorizer()
    X_train_transformed = vectorizer.fit_transform(X_train)
    X_test_transformed = vectorizer.transform(X_test)
    X_train_transformed

    #Creamos y ajustamos el modelo
    model = MultinomialNB()
    model.fit(X_train_transformed, y_train)
    y_pred = model.predict(X_test_transformed)
    #Vemos que se logra predecir correctamente un 27.5% del conjunto de prueba, por lo que empeora
    print("Accuracy Lemmatization:", metrics.accuracy_score(y_test, y_pred)) #empeora

    #En general, se puede decir que el mejor es stemming

if __name__ == "__main__":
    NLP_token_stem_lemma()