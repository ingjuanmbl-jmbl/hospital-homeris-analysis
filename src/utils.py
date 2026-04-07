import pandas as pd
from pandas import DataFrame
import joblib
from pathlib import Path



def read_csv(route: str):
    """
    Lee Archivos tipo csv de una ruta especificada
    Args:
        route: ruta en la cual se encuentra el DataFrame a Analizar
    """
    
    try:
        df = pd.read_csv(route)
        print(f"Archivo cargado existosamente desde: {route}")
        return df
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {route}")
        return None

def save_csv(df: DataFrame, route: str):
    
    """
    Guarda un DataFrame en un archivo CSV
    Args: df: Debe ser un DataFrame
    route: ruta en la cual se guardará el DataFrame
    """
    df.to_csv(route, index=False)
    print(f"DataFrame guardado existosamente en la ruta: {route}")

####------------------------------------FUNCIONES DE GUARDADO DE ARTEFACTOS --------------- ###
# Definimos la ruta raíz del proyecto (un nivel arriba de src)
ROOT_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = ROOT_DIR / "artifacts"

#Definir la función de guardado del artefacto
def save_artifact(obj, name, artifacts_type):
    """
    Guarda un objeto de Python (modelo, encoder, scaler, etc.) en una subcarpeta específica 
    dentro del directorio de 'artifacts'.
        Args:
            obj: obj (any): El objeto de Python que se desea persistir (ej. un modelo de KMeans o un OrdinalEncoder).
            name (str): El nombre que se le dará al archivo (sin la extensión .joblib).
            artifacts_type (str): El nombre de la subcarpeta donde se guardará.
        Returns:
            pathlib.Path: La ruta completa donde se guardó el archivo.
    """
    #Definir y crear al carpeta si no existe
    target_dir = ARTIFACTS_DIR / artifacts_type
    target_dir.mkdir(parents=True, exist_ok=True)

    #Constrir la ruta final del archivo 
    file_path = target_dir / f"{name}.joblib"

    #Guardar el objeto en el disco 
    joblib.dump(obj, file_path)
    print(f"Objeto correctamente cargado en: {file_path}")
    
    return file_path

def load_artifact(name, artifact_type):
    """
    Carga un objeto guardado previamente en formato .joblib desde la carpeta de artifacts.
    Args:
        name (str): El nombre del archivo que se desea cargar (sin la extensión .joblib).
        artifact_type (str): La subcarpeta donde se encuentra el archivo. 
            Debe coincidir con el tipo usado al guardar.
    Returns:
        any: El objeto cargado (modelo, encoder, etc.) listo para ser usado.
    Raises:
        FileNotFoundError: Si el archivo buscado no existe en la ruta especificada.
    """
    # Construir la ruta del archivo que se quiere buscar
    file_path = ARTIFACTS_DIR / artifact_type / f"{name}.joblib"
    
    # Verificar si el archivo existe antes de intentar cargarlo
    if not file_path.exists():
        raise FileNotFoundError(f"❌ Error: El archivo '{name}.joblib' no existe en '{artifact_type}'.")
    
    # Cargar y retornar el objeto
    obj = joblib.load(file_path)
    print(f"📂 Artefacto cargado correctamente desde: {file_path}")
    return obj

##### -----------------------------------------------##########################

    
