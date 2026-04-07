import sys
import os
import joblib

# Esto asegura que 'src' sea visible sin importar desde dónde se ejecute el script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.utils import(
    read_csv, 
    save_csv, 
    save_artifact
)

from src.cleaning import eliminar_cols_pp

from src.preprocessing import (
    transformar_ordinal,
    transformar_onehot,
    scaled_data
)

from src.PCA import aplicar_PCA

def pipeline_prep():
    print("Iniciando Preprocesamiento de datos")

    # Esto elimina el uso de "../" 
    path_input = os.path.join(BASE_DIR, "data", "clean", "homeris-data-clean.csv")
    
    df = read_csv(path_input)
    df = eliminar_cols_pp(df)

    df, encoder_ord = transformar_ordinal(df)
    save_artifact(encoder_ord, "encoder_ord", "preprocessors")

    df, encoder_onehot = transformar_onehot(df)
    save_artifact(encoder_onehot, "encoder_onehot", "preprocessors")

    df, RScaled = scaled_data(df)
    save_artifact(RScaled, "Rscaled", "preprocessors")
    save_csv(df, "data/preprocessed/homeris-data-clean-preprocessed.csv")

    df_final_pca, modelo_pca = aplicar_PCA(df, n_components=0.70)
    save_csv(df_final_pca, "data/PCA/homeris-data-clean-preprocessed-PCA.csv")
    save_artifact(modelo_pca, "PCA", "preprocessors")


    print("Prepocesamiento Finalizado con exito")
    return df




if __name__ == "__main__":
    pipeline_prep()