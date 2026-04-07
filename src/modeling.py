import pandas as pd
import numpy as np
import joblib
import os
import sys
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabasz_score


from src.cleaning import eliminar_cols_pp

#Configuracion de la ruta raiz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

def optimizar_algoritmo(df, tipo):
    """
    Itera diferentes clusteres de tres modelos diferenetes y selecciona el que tenga mejores metricas
        Args:
            df (DataFrame): Debe ser el conjunto de datos previamente preprocesado
            tipo (str): el nombre del algoritmo que se quiere iterar y ejecutar
                opciones: kmeans, AgglomerativeClustering (ac), gmm
    """
    mejor_score = -1
    mejor_modelo = None
    historico_intentos =[]

    print(f"Analizando {tipo.upper()}...")

    for k in range(2, 11):
        if tipo == "kmeans":
            modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = modelo.fit_predict(df)
        elif tipo == "ac":
            modelo = AgglomerativeClustering(n_clusters=k)
            labels = modelo.fit_predict(df)
        elif tipo == "gmm":
            modelo = GaussianMixture(n_components=k, random_state=42)
            labels = modelo.fit_predict(df)
        else:
            raise ValueError("Tipo no de modelo no valido")
        
        #Metricas
        sil =  silhouette_score(df, labels)
        cal = calinski_harabasz_score(df, labels)

        # guardado histórico
        historico_intentos.append({
            "modelo": tipo,
            "k": k,
            "silhouette": sil,
            "calinski_harabasz": cal
        })

        # criterio de optimización (puedes ajustar)
        if sil > mejor_score:
            mejor_score = sil
            mejor_modelo = modelo
            mejor_k = k

    df_resultados = pd.DataFrame(historico_intentos)

    return mejor_modelo, mejor_k, df_resultados


def entrenar_algoritmos(df: pd.DataFrame) -> pd.DataFrame:
    modelos = ["kmeans", "ac", "gmm"]
    resultados = []
    mejores_modelos = {}

    # 1. Ejecutar la optimización para cada algoritmo
    for m in modelos:
        modelo, k, df_res = optimizar_algoritmo(df, m)
        resultados.append(df_res)
        mejores_modelos[m] = modelo
    
    # 2. Consolidar todas las métricas en un solo DataFrame
    df_metricas = pd.concat(resultados, ignore_index=True)
    
    # 3. Seleccionar automáticamente el mejor modelo basado en los scores
    mejor = seleccionar_mejor_modelo(df_metricas)

    # 4. Recuperar el objeto del modelo entrenado que corresponde al mejor resultado
    modelo_final = mejores_modelos[mejor["modelo"]]

    return df_metricas, modelo_final, mejor
    
def seleccionar_mejor_modelo(df_metricas):
    if df_metricas.empty:
        raise ValueError("El DataFrame esta vacio")
    
    mejor_fila = df_metricas.loc[df_metricas["silhouette"].idxmax()]

    return {
        "modelo": mejor_fila["modelo"],
        "k": int(mejor_fila["k"]),
        "silhouette": float(mejor_fila["silhouette"]),
        "calinski_harabasz": float(mejor_fila["calinski_harabasz"])
    }



def inference(df, encoder_ord, encoder_onehot, scaler, pca_model):
    """
    Pipeline de preprocesamiento completo para inferencia, 
    incluyendo la reducción de dimensionalidad con PCA.
    """
    # 1. Limpieza inicial
    df = eliminar_cols_pp(df)

    # 2. Ordinal (solo RANGO_EDAD)
    df['RANGO_EDAD'] = encoder_ord.transform(df[['RANGO_EDAD']])

    # 3. OneHot (solo columnas categóricas)
    cols_cats = ['MUNICIPIO', 'DIAGNOSTICO', 'GENERO', 'REGIMEN']

    encoded_data = encoder_onehot.transform(df[cols_cats])
    encoded_cols = encoder_onehot.get_feature_names_out(cols_cats)

    df_encoded = pd.DataFrame(encoded_data, columns=encoded_cols, index=df.index)

    # eliminar originales + agregar nuevas
    df = pd.concat([df.drop(columns=cols_cats), df_encoded], axis=1)

    # 4. Escalado
    data_scaled = scaler.transform(df)
    df_scaled = pd.DataFrame(data_scaled, columns=df.columns, index=df.index)

    # 5. Reducción de Dimensionalidad (PCA)
    # Usamos .transform() para proyectar los nuevos datos en los componentes ya entrenados
    data_pca = pca_model.transform(df_scaled)
    
    # Creamos el DataFrame final con los nombres de las columnas (PC1, PC2... PC41)
    cols_pca = [f'PC{i+1}' for i in range(data_pca.shape[1])]
    df_final = pd.DataFrame(data_pca, columns=cols_pca, index=df.index)

    return df_final