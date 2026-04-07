import sys
import os

# Esto asegura que 'src' sea visible sin importar desde dónde se ejecute el script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.extraction import extract_socrata_data
from src.cleaning import (
    rename_columns,
    transform_types, 
    extract_temporal_features, 
    clean_diagnostico, 
    clasificar_diagnostico,
    sep_salud_mental
)
from src.utils import save_csv, read_csv



def pipeline_clean():
    """
    Pipeline de limpieza de datos
    """
    print("Iniciando pipeline de limpieza de datos")
    # Traemos el token desde el entorno, si no existe, será None


    df = extract_socrata_data(
        "izfv-6qvv",
        "data/raw/homeris-data.csv",
    )
    df = read_csv("data/raw/homeris-data.csv")
    df = rename_columns(df)
    df = transform_types(df)
    df = extract_temporal_features(df)
    df = clean_diagnostico(df)
    df = clasificar_diagnostico(df)
    df = sep_salud_mental(df)
    df = save_csv(df, "data/clean/homeris-data-clean.csv")   
    print("Pipeline de limpieza de datos finalizado")
    return df

if __name__ == "__main__":
    pipeline_clean()