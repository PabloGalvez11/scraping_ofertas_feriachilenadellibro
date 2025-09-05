import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os

from sklearn.model_selection import train_test_split #Para separar en conjunto de entrenamiento y de prueba.
import statsmodels.api as sm #Importamos librería statsmodels que entrega los modelos de regresión. Servirá para utilizar modelos de regresión lineal.
from statsmodels.miscmodels.ordinal_model import OrderedModel #para utilizar el modelo multinomial ordinal.
from imblearn.over_sampling import SMOTE #para realizar remuestreo con SMOTE y balanceo de clases.

#Importamos métricas para medir la eficacia del modelo de clasificación multinomial ordinal.
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score, classification_report, cohen_kappa_score, f1_score
from sklearn.metrics import confusion_matrix



import joblib
from .config import fecha_scraping, PROCESSED_DIR, MODELS_DIR, engine, estandarizar

def modelo_descuento():

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
    y = df["rango_descuento"] #apartamos la variable antes de la estandarización y el OHE para más simplicidad.
    df = df.drop(columns=["titulo","categoria", "autor", "descripcion", "link",
                            "porcentaje_descuento","precio_oferta","rango_descuento",
                            "largo","ancho","grosor", "disponibles", "fecha_extraccion"])
    #Separamos e identificamos variables numéricas y categóricas
    variables_numericas = df.select_dtypes(include="number").columns.tolist()
    variables_categoricas = df.select_dtypes(include=["object","category"]).columns.tolist()
    #df[variables_numericas].corr()


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
    X = df
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #Aplicamos SMOTE para resamplear los datos.
    smote = SMOTE(random_state=42)
    #Aplicamos SMOTE
    X_train, y_train = smote.fit_resample(X_train, y_train)
    #Revisamos el balance
    print(y_train.value_counts())

    ### Modelo con statsmodel ###


    #Agregamos la constante
    #No la utilizaremos porque no hace falta, pero se deja definido igualmente.
    X_train_const = sm.add_constant(X_train)
    X_test_const = sm.add_constant(X_test)

    #Creamos y ajustamos el modelo
    modelo = OrderedModel(
        y_train,
        X_train,
        distr='logit'  # 'logit' o 'probit'
    )
    res = modelo.fit(method='lbfgs',maxiter=3000, disp=True)
    # Resumen con p-valores y significancia
    print(res.summary())
    joblib.dump(res, os.path.join(MODELS_DIR, f"modelos_descuento/modelo_descuento_{fecha_scraping}.joblib"))

    # Predicciones

    # Probabilidades de cada categoría
    probs = res.predict(X_test)
    #Obtenemos el índice de la categoría con mayor probabilidad
    y_pred_idx = np.argmax(probs.values, axis=1)
    #Convertimos los índices a etiquetas respectivas
    y_pred = pd.Categorical.from_codes(y_pred_idx, y.cat.categories)
    #Comparamos con los valores reales para ver la efectividad de la predicción.
    print("Accuracy test:", accuracy_score(y_test, y_pred))
    #Matriz de confusión
    cm = confusion_matrix(y_test, y_pred, labels=y_train.cat.categories)
    #Convertimos a dataframe para mejor visualización y graficar la matriz de confusión.
    cm_df = pd.DataFrame(cm, index=y_train.cat.categories, columns=y_train.cat.categories)
    #Graficamos
    plt.figure(figsize=(6,4))
    sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicho")
    plt.ylabel("Real")
    plt.title("Matriz de Confusión - Modelo Ordinal")
    plt.show()

    # Accuracy
    acc = accuracy_score(y_test, y_pred)
    print("Accuracy:", acc)
    # Reporte completo: precision, recall, f1-score por categoría
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    # Cohen Kappa (mide concordancia ajustada por azar, útil en ordinal)
    kappa = cohen_kappa_score(y_test, y_pred, weights="quadratic")  # "linear" o "quadratic"
    print("Cohen's Kappa (ponderado):", kappa)
    # Macro F1 (promedio de F1 por clase)
    macro_f1 = f1_score(y_test, y_pred, average="macro")
    print("Macro F1:", macro_f1)

if __name__ == "__main__":
    modelo_descuento()