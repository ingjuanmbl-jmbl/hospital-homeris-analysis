import pandas as pd
from pandas import DataFrame
import numpy as np


def rename_columns(df: DataFrame) -> DataFrame:
    """
    Toma las columnas mediante un mapeo y estandariza sus numbres
        Args:
        df: Debe ser un DataFrame
    """
    df = df.rename(columns={
        'anio_mes':"PERIODO",
        'municipio_residencia': "MUNICIPIO",
        'grupo_diagnostico': "DIAGNOSTICO",
        'genero_paciente': "GENERO",
        'regimen_atencion': "REGIMEN",
        'rango_edad': "RANGO_EDAD",
        'total_casos': "CANTIDAD_CASOS"
    })
    print(f"Columnas renombradas correctamente: {df.columns}")
    return df

def transform_types(df: DataFrame) -> DataFrame:
    """
    Tranformaciones a los tipos de datos necesarios
        Args: df: Debe ser un DataFrame

    """
    #Convertimos 'PERIODO' a una fecha real de pandas
    df['PERIODO'] = pd.to_datetime(df['PERIODO'], format='%Y-%m')
    print(f"Columna convertida a fecha de pandas correctamente: \n {df.dtypes}")
    return df

def extract_temporal_features(df: DataFrame) -> DataFrame:
    """
    Extrae las variables temporales del DataFrame
    Args: df: Debe ser un DataFrame
    """
    #Calcular el año, mes y trimestre
    df['ANIO'] = df['PERIODO'].dt.year
    df['MES_NUM'] = df['PERIODO'].dt.month
    # Convierte la fecha a un objeto de periodo mensual
    df['PERIODO_MENSUAL'] = df['PERIODO'].dt.to_period('M')
    df['TRIMESTRE'] = df['PERIODO'].dt.quarter

    #Nombre del mes
    df['MES_NOMBRE'] = df['PERIODO'].dt.month_name()

    # Semestre (Cálculo manual común en reportes financieros/salud)
    df['SEMESTRE'] = df['PERIODO'].dt.month.apply(lambda x: 1 if x <= 6 else 2)
    
    print(f"Variables temporales extraídas:\n{df.columns}")
    return df

def clean_diagnostico(df: DataFrame) -> DataFrame:
    """
    Limpia la variable diagnóstico convirtiendola a mayusculas y quitando tildes
    Args: df: Debe ser un DataFrame
    """
    # 1. Todo a mayúsculas y quitar espacios extra a los lados
    df['DIAGNOSTICO'] = df['DIAGNOSTICO'].str.upper().str.strip()
    
    # 2. (Opcional) Quitar tildes para evitar duplicados por codificación
    df['DIAGNOSTICO'] = df['DIAGNOSTICO'].str.normalize('NFKD')\
                        .str.encode('ascii', errors='ignore')\
                        .str.decode('utf-8')
    return df
    

def mapeo_diagnostico(dx):
    """
    Mapea el diagnóstico en un grupo
    Args: dx: Debe ser un diccionario con los grupos y las palabras clave que lo definen
    """
    grupos = {
    "INFECTOLOGIA": [
        "VIH", "INMUNODEFICIENCIA", "TUBERCULOSIS", "SIFILIS", "CANDIDIASIS", 
        "DERMATOFITOSIS", "MICOSIS", "ESCABIOSIS", "PEDICULOSIS", "HERPES", 
        "INFECCION", "INFECCIONES", "INFLUENZA", "NEUMONIA", "SINUSITIS", 
        "RINOFARINGITIS", "INTESTINALES", "VIRUS", "BACTERIANA", "CLAMIDIAS", 
        "FIEBRES RECURRENTES", "MICOBACTERIAS"
    ],

    "RESPIRATORIO": [
        "ASMA", "BRONQUITIS", "RESPIRACION", "EPOC", "PULMONARES OBSTRUCTIVAS"
    ],

    "CARDIOVASCULAR": [
        "HIPERTENSION", "INFARTO", "CARDIACO", "CEREBROVASCULAR", "ISQUEMIA", 
        "FLEBITIS", "TROMBOFLEBITIS", "VARICES", "HIPOTENSION", "VASCULAR", 
        "MIOCARDIO", "VENAS VARICOSAS"
    ],

    "ENDOCRINO_METABOLICO": [
        "DIABETES", "OBESIDAD", "DESNUTRICION", "METABOLISMO", "TIROID", 
        "HIPOTIROID", "ADRENOGENITALES", "PORFIRINAS", "BILIRRUBINA"
    ],

    "NEUROLOGICO": [
        "EPILEPSIA", "CONVULSIONES", "CONVULSION", "PARKINSON", "ALZHEIMER", 
        "DISTONIA", "HEMIPLEJIA", "NEUROPAT", "MOVIMIENTOS INVOLUNTARIOS", 
        "ENCEFALOPATIA", "SINDROMES VASCULARES ENCEFALICOS", "HUNTINGTON", 
        "SISTEMA NERVIOSO", "DEGENERATIVOS", "MIGRANA", "PARALISIS", 
        "EXTRAPIRAMIDALES", "RAICES", "PLEXOS", "MUSCULARES PRIMARIOS", 
        "SENSIBILIDAD CUTANEA", "MARCHA", "MOVILIDAD"
    ],

    "SALUD_MENTAL": [
        "ESQUIZOFRENIA", "PSICOSIS", "DEPRESIVO", "DEPRESION", "BIPOLAR", 
        "ANSIEDAD", "OBSESIVO", "COMPULSIVO", "PERSONALIDAD", "TRASTORNO MENTAL", 
        "PSICOTICO", "SUICID", "AUTOINFLING", "CONDUCTA", "DELIRIO", "ALCOHOL", 
        "COCAINA", "CANNAB", "OPIACE", "DROGA", "HIPNOTICOS", "SEDANTES", 
        "TABACO", "ALUCINOGENOS", "RETRASO MENTAL", "ESTRES", "ADAPTACION", 
        "HIPERCINETICOS", "EMOCIONALES", "DESARROLLO", "DEMENCIA", "HUMOR", 
        "AFECTIVO", "SOMATOMORFOS", "SUENO", "DISOCIATIVOS", "IDENTIDAD DE GENERO", 
        "IMPULSOS", "ESQUIZOAFECTANIVOS", "ESQUIZOTIPICO", "DELIRANTES", 
        "PSICOLOGICOS", "NEUROTICOS", "INGESTION DE ALIMENTOS", "MANIACO","OTROS TRASTORNOS MENTALES",
        "TRASTORNOS DEL COMPORTAMIENTO","TRASTORNOS MENTALES","TRASTORNOS DE LA PREFERENCIA SEXUAL",
        "TRASTORNOS POR TICS","SINDROME DEL COMPORTAMIENTO"

    ],

    "DIGESTIVO": [
        "GASTRITIS", "DUODENITIS", "REFLUJO", "DISPEPSIA", "COLON IRRITABLE", 
        "HERNIA", "ESOFAGO", "INTESTINO", "ABDOMINAL", "NAUSEA", "VOMITO", 
        "DIARREA", "GASTROENTERITIS", "ESTOMATITIS", "CARIES", "GINGIVITIS", 
        "PERIODONTALES"
    ],

    "GENITOURINARIO": [
        "RENAL", "RINON", "URETER", "PROSTATA", "INCONTINENCIA", "ORINA", 
        "VAGINA", "VULVA", "GENITALES", "PELVICAS", "VULVOVAGINAL", 
        "MENOPAUSICOS", "PERIMENOPAUSICOS", "URINARIO"
    ],

    "PIEL": [
        "ACNE", "DERMATITIS", "CELULITIS", "ABSCESO", "FURUNCULO", "ANTRAX", 
        "CUTANEO", "PIEL", "URTICARIA", "PRURITO", "UNAS"
    ],

    "MUSCULOESQUELETICO": [
        "ARTROSIS", "COXARTROSIS", "OSTEOPOROSIS", "ESCOLIOSIS", "DORSALGIA", 
        "DISCO", "ARTICUL", "SINOVITIS", "TENOSINOVITIS", "MUSCULO", 
        "ENTESOPATIAS", "RODILLA", "DEFORMIDADES ADQUIRIDAS", "DORSOPATIAS"
    ],

    "TRAUMA_ACCIDENTES": [
        "FRACTURA", "TRAUMAT", "HERIDA", "QUEMAD", "LUXACION", "ESGUINCE", 
        "TORCEDURA", "CAIDA", "ACCIDENTE", "GOLPE", "AGRESION", "MALTRATO", 
        "NEGLIGENCIA", "ABANDONO", "SECUELAS", "AHORCAMIENTO", "ESTRANGULAMIENTO", 
        "SOFOCACION", "OBJETO CORTANTE", "OBJETO ROMO"
    ],

    "INTOXICACIONES": [
        "ENVENENAMIENTO", "TOXICO", "PLAGUICIDA", "EFECTO TOXICO", 
        "EFECTOS ADVERSOS", "ENVENENAMIENTO AUTOINFLINGIDO"
    ],

    "EMBARAZO": [
        "EMBARAZO", "PUERPERIO", "MEMBRANAS"
    ],

    "MALFORMACIONES_CONGENITAS": [
        "DOWN", "TRISOMIA", "CROMOSOMIC", "MALFORMACION", "CONGENITA", "FACOMATOSIS"
    ],

    "TUMORES": [
        "TUMOR", "NEOPLASIA"
    ],

    "SINTOMAS_GENERALES": [
        "CEFALEA", "MAREO", "FATIGA", "MALESTAR", "SINCOPE", "SIGNOS", 
        "SINTOMAS", "DOLOR", "RESPIRACION", "LATIDO", "AMIGDALITIS", 
        "PURPURA", "FALTA DEL DESARROLLO FISIOLOGICO", "HABLA", "LENGUAJE", 
        "HIPOACUSIA", "OTITIS", "SORDERA", "OJO", "PARPADOS", "OIDO", "LABERINTITIS","OTROS TRASTORNOS DE LOS TEJIDOS BLANDOS"
    ],

    "CONTACTO_SERVICIOS_SALUD": [
        "EXAMEN", "CONTROL", "SUPERVISION", "CONSULTA", "HISTORIA", "CONTACTO", 
        "OBSERVACION", "PESQUISA", "ANTICONCEPCION"
    ],

    "FACTORES_SOCIALES": [
        "PROBLEMAS RELACIONADOS", "AMBIENTE SOCIAL", "DESEMPLEO", "VIVIENDA", 
        "EDUCACION", "ALFABETIZACION", "ESTILO DE VIDA", "CRIANZA", 
        "MODO DE VIDA"
    ]
}

    for grupo, palabras in grupos.items():
        for palabra in palabras:
            if palabra in dx:
                return grupo

    return "OTROS"

def clasificar_diagnostico(df: DataFrame) -> DataFrame:
    """
    Clasifica el diagnóstico en un grupo
    Args: df: Debe ser un DataFrame
    """
    df["GRUPO_DIAGNOSTICO"] = df["DIAGNOSTICO"].apply(mapeo_diagnostico)
    print(f"Diagnóstico clasificado correctamente: \n {df['GRUPO_DIAGNOSTICO']}")
    return df

def sep_salud_mental(df: DataFrame)-> DataFrame:
    """
    De acuerdo a la clasificación anterior clasifica en dos categorias posibles
    si es de salud mental le asigna el mismo valor, de lo contrario le asigna otro grupo
    """
    df["SALUD_MENTAL_CLASS"] = np.where(
        df["GRUPO_DIAGNOSTICO"] == "SALUD_MENTAL",
        "SALUD_MENTAL",
        "OTROS_GRUPOS_DX")
    print("Grupo diagnostico separado")
    return df


def eliminar_cols_pp(df: DataFrame) -> DataFrame:
    """
    Elimina variables de periodo que no son necesarias dentro del ciclo de preprocesamiento
    """
    cols_drop = ['PERIODO','CANTIDAD_CASOS','ANIO','MES_NUM','PERIODO_MENSUAL','TRIMESTRE', 'MES_NOMBRE', 'SEMESTRE','GRUPO_DIAGNOSTICO', 'SALUD_MENTAL_CLASS']

    return df.drop(columns=cols_drop, errors='ignore')


def cambio_nombre_grupo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Toma los clusteres originales en el dataframe y le asigna mediante mapeo los nombres de grupo A y Grupo B
        Args:
        df: Corresponde al DataFrame final el cual contiene la asiganción final del los grupos una vez se entrenan los modelos
    """
    mapeo_cluster = {
    2:'Grupo A',
    9:'Grupo B'
    }

    df["cluster"] = df["cluster"].map(mapeo_cluster)
    print("Grupos asignados y mapeados correctamente")
    return df
