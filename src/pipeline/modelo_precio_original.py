import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os

from sklearn.model_selection import train_test_split #Para separar en conjunto de entrenamiento y de prueba.
from sklearn.linear_model import LinearRegression #importamos la función para la creación de modelos de regresión lineal de sklearn.
from sklearn.metrics import mean_squared_error, r2_score #importamos las funciones para el cálculo de métricas de bondad de ajuste R^2 y MSE.


import joblib
from .config import fecha_scraping, PROCESSED_DIR, MODELS_DIR, engine, estandarizar

def modelo_precio_original():
    #Importamos los datos
    df = pd.read_sql(f"SELECT * FROM ofertas_{fecha_scraping}", engine)
    #df = pd.read_csv(os.path.join(PROCESSED_DIR, f"ofertas_{fecha_scraping}.csv"), sep=";", decimal=",", encoding="utf-8")


    #Reasignaremos valores de la variable categórica de "encuadernación" con menor frecuencia que 10, ya que serían muy pocos para considerar en un modelo.
    frecuencias = df["encuadernacion"].value_counts() ; df["encuadernacion"] = np.where(df["encuadernacion"].map(frecuencias) >= 10, df["encuadernacion"], "otro")
    #Reasignaremos valores de la variable categórica de "editorial" con menor frecuencia que 10, ya que serían muy pocos para considerar en un modelo.
    frecuencias = df["editorial"].value_counts() ; df["editorial"] = np.where(df["editorial"].map(frecuencias) >= 10, df["editorial"], "otro")
    #Reasignaremos valores de la variable categórica de "encuadernación" con menor frecuencia que 10, ya que serían muy pocos para considerar en un modelo.
    frecuencias = df["macrocategoria"].value_counts() ; df["macrocategoria"] = np.where(df["macrocategoria"].map(frecuencias) >= 10, df["macrocategoria"], "otro")
    #Creamos una variable categórica que indica los rangos de descuento. Será utilizada como variable objetivo para uno de los modelos.
    bins = [-float("inf"), 0.19, 0.24, 0.29, float("inf")] ; labels = ["<0.2", "0.20-0.24", "0.25-0.29", "0.3 o más"]
    df["rango_descuento"] = pd.cut(df["porcentaje_descuento"], bins=bins, labels=labels)


    #Nos deshacemos de las variables que no serán consideradas para un modelo.
    df = df.drop(columns=["titulo","categoria", "autor", "descripcion", "link", 
                            "precio_oferta","porcentaje_descuento","rango_descuento",
                            "largo","ancho","grosor","disponibles", "fecha_extraccion"])
    #Separamos e identificamos variables numéricas y categóricas
    variables_numericas = df.select_dtypes(include="number").columns.tolist()
    variables_categoricas = df.select_dtypes(include=["object","category"]).columns.tolist()
    #df[variables_numericas].corr()


    #Estandarizamos las variables numéricas
    df = estandarizar(df)
    #realizamos one-hot encoding en las variables categóricas
    df = pd.get_dummies(df, columns=variables_categoricas, drop_first=True)
    df = df.astype(float)

    #Separamos la variable objetivo y los conjuntos de entrenamiento
    X = df.drop("precio_original", axis=1)
    y = df["precio_original"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


    ### Modelo con sklearn ###

    #Creamos y ajustamos el modelo
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    joblib.dump(modelo, os.path.join(MODELS_DIR, f"modelos_precio_original/modelo_precio_original_{fecha_scraping}.joblib"))
    #Realizamos las predicciones
    y_pred_train = modelo.predict(X_train)
    y_pred_test = modelo.predict(X_test)

    # Métricas de error y bondad de ajuste tanto del entrenamiento como predicción.
    print("Entrenamiento:")
    print("R²:", r2_score(y_train, y_pred_train))
    print("MSE:", mean_squared_error(y_train, y_pred_train))
    print("RMSE:",  np.sqrt(mean_squared_error(y_train, y_pred_train)))
    print("\nPrueba:")
    print("R²:", r2_score(y_test, y_pred_test))
    print("MSE:", mean_squared_error(y_test, y_pred_test))
    print("RMSE:",  np.sqrt(mean_squared_error(y_test, y_pred_test)))
    #Gráfica comparativa de predicción vs valor real
    plt.scatter(y_pred_test, y_test, alpha=0.7)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
    plt.xlabel("Valores reales")
    plt.ylabel("Valores predichos")
    plt.title("Regresión lineal - Predicción vs valor real")
    plt.show()

if __name__ == "__main__":
    modelo_precio_original()