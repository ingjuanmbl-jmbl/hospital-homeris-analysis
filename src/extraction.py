import pandas as pd
from sodapy import Socrata


def extract_socrata_data(dataset_id: str, 
                         save_path: str, 
                         client_url: str = "www.datos.gov.co", 
                         token: str = None):
    """
    Extrae los datos de un dataset de Socrata y lo guarda en un archivo CSV.
    Args:
        dataset_id: ID del dataset de Socrata. Este consulta en el portal de datos abiertos de Colombia.
        save_path: Ruta donde se guardará el archivo CSV. Por defecto es "data/raw/dataset_id.csv".
        client_url: URL del cliente de Socrata. Por defecto es "www.datos.gov.co".
        token: Token de Socrata. Por defecto es None.  
    """
    client = Socrata(client_url, token, timeout=120)
    #ID del data set
    data_set_id = dataset_id

    #Establecemos los parametros de paginación
    limit = 5000
    offset = 0
    all_results = []

    while True:
        results = client.get(data_set_id, limit=limit, offset=offset)
        if not results:
            break
        all_results.extend(results)
        offset += limit
        print(f"{offset} registros descargados...")

    #Convertir a DaraFrame
    df = pd.DataFrame.from_records(all_results)

    #Guardar el DataFrame en un archivo CSV
    df.to_csv(save_path, index=False)
    print(f"DataSet descargado correctamente y almacenado en {save_path}" )
    return df
