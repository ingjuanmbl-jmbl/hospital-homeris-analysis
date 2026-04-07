import sys
import os

# Esto asegura que 'src' sea visible sin importar desde dónde se ejecute el script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.utils import save_artifact, read_csv, save_csv
from src.modeling import entrenar_algoritmos




def pipe_line_modeling():
    print("Iniciando modelado de datos")
    path_input = os.path.join(BASE_DIR, "data", "PCA", "homeris-data-clean-preprocessed-PCA.csv")
    path_output_df_metrics = os.path.join(BASE_DIR,"data","best_model_result", "best_model_result.csv")
    
    
    df = read_csv(path_input)

    df_metricas, modelo_final, mejor = entrenar_algoritmos(df)
    

    print(f"Mejor modelo: {mejor['modelo']} con k={mejor['k']}")


    save_csv(df_metricas,path_output_df_metrics)
    save_artifact(modelo_final,"Best_model_ns", "models")

    return modelo_final, df_metricas, mejor
    


if __name__ == "__main__":
    pipe_line_modeling()
    




    


