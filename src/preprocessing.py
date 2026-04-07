import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import RobustScaler, OneHotEncoder, OrdinalEncoder


#Codificar variable ordinal (Rango edad)
def transformar_ordinal(df: DataFrame) -> DataFrame:
    orden_edad = ['0-5','6-11','12-17','18-28','29-59','60+']
    encoder_ord = OrdinalEncoder(categories=[orden_edad])

    #Aplicar y reemplazar en el df
    df['RANGO_EDAD'] = encoder_ord.fit_transform(df[['RANGO_EDAD']])
    
    return df, encoder_ord

#Codificar variables nominales
def transformar_onehot(df: DataFrame) -> DataFrame:
    cols_cats = ['MUNICIPIO', 'DIAGNOSTICO', 'GENERO', 'REGIMEN']
    encoder_onehot = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    #generamos las nuevas columnas
    encoded_data = encoder_onehot.fit_transform(df[cols_cats])
    encoded_cols = encoder_onehot.get_feature_names_out(cols_cats)

    #creamos un df con las nuevas columnas y eliminamos las originales
    df_encoded = pd.DataFrame(encoded_data, columns=encoded_cols, index=df.index)
    df = pd.concat([df.drop(columns=cols_cats), df_encoded], axis=1)

    return df, encoder_onehot

#Escalado final
def scaled_data(df: DataFrame) -> DataFrame:
    Rscaler = RobustScaler()
    data_Rscaled = Rscaler.fit_transform(df)
    df_final = pd.DataFrame(data_Rscaled, columns=df.columns)
    
    return df, Rscaler


