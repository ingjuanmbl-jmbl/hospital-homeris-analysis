import sys
import os
import numpy as np

# Configurar ruta raíz correctamente
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.modeling import inference
from src.utils import load_artifact, read_csv, save_csv


def pipeline_inference():
    print("Iniciando inferencia...")

    # 📂 Rutas robustas
    path_data = os.path.join(BASE_DIR, "data", "clean", "homeris-data-clean.csv")
    path_output = os.path.join(BASE_DIR, "data", "clean", "homeris-data-clean-cluster.csv")

    path_pre = os.path.join(BASE_DIR, "artifacts", "preprocessors")
    path_model = os.path.join(BASE_DIR, "artifacts", "models")

    # 📥 Cargar data
    df_clean = read_csv(path_data)

    # 📦 Cargar artefactos
    encoder_ord = load_artifact("encoder_ord", path_pre)
    encoder_onehot = load_artifact("encoder_onehot", path_pre)
    scaler = load_artifact("Rscaled", path_pre)
    modelo = load_artifact("Best_model_ns", path_model)
    pca = load_artifact("PCA", path_pre)

    # 🔄 Preprocesamiento
    df_model = inference(df_clean, encoder_ord, encoder_onehot, scaler, pca)

    # 🎯 Predicción
    labels = modelo.predict(df_model)

    unique_labels, counts = np.unique(labels, return_counts=True)
    print(f"DEBUG - Etiquetas encontradas: {unique_labels}")
    print(f"DEBUG - Distribución: {counts}")

    # 🧩 Asignar clusters
    df_clean["cluster"] = labels

    # 💾 Guardar resultado
    save_csv(df_clean, path_output)

    print("Inferencia finalizada con éxito 🚀")


if __name__ == "__main__":
    pipeline_inference()