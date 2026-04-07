import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
from src.cleaning import cambio_nombre_grupo

# Configuración de la página
st.set_page_config(
    page_title="Caracterización de pacientes",
    layout="wide",
    page_icon="🔍")

st.markdown("<h1 style='text-align: center;'>🔍 Caracterización de pacientes</h1>", unsafe_allow_html=True)
st.info(
    """Esta sección presenta el análisis de la población atendida en el hospital, 
        con el objetivo de identificar patrones relevantes a partir de la implementación
         del algoritmo de clustering."""
        )

#Aasignamos rutas de lectura
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
path_input = os.path.join(BASE_DIR,"data","clean", "homeris-data-clean-cluster.csv")

#cargar datos

def cargar_datos():

    df = pd.read_csv(path_input)
    #Renombramos el nombre de los grupo
    cambio_nombre_grupo (df)

    return df

df = cargar_datos()

#Filtramos cada dataset de cada grupo para analzarlo en comparativas más adelante

df_A = df[df["cluster"] == "Grupo A"]
df_B = df[df["cluster"] == "Grupo B"]

st.markdown("---")

#Cantidad de casos por grupo

###################### 1. COMPORTAMIENTO POR CLUSTER #####################
#Agrupar por cantidad de casos y cluster
df_group_cluster = df.groupby("cluster")["CANTIDAD_CASOS"].sum().reset_index()

#Calcular el %
df_group_cluster["PORCENTAJE_GRUPO"] = (
    df_group_cluster["CANTIDAD_CASOS"] / df_group_cluster["CANTIDAD_CASOS"].sum()
    ) * 100
    
df_group_cluster["PORCENTAJE_GRUPO"] = df_group_cluster["PORCENTAJE_GRUPO"].round(2)
    

fig_group_cluster = px.bar(
    df_group_cluster,
    y="CANTIDAD_CASOS",
    x = "cluster",
    hover_data = "PORCENTAJE_GRUPO",
    title ="Cantidad de casos Atendidos en el hospital por grupo"
    )

st.plotly_chart(fig_group_cluster, use_container_width=True)

st.info(
    """
    El análisis permitió identificar dos grupos predominantes.
     El **Grupo A** concentra **24.747 casos (70,15%)**, mientras que el **Grupo B** agrupa **10.414 casos (28,85%)**,
     evidenciando una distribución marcadamente desigual entre ambos.
    """
)

variable = st.selectbox(
    "Selecciona la variable que deseas analizar",
    ["GENERO", "REGIMEN", "RANGO_EDAD"]
)


df_group = df.groupby(["cluster", variable])["CANTIDAD_CASOS"].sum().reset_index()

df_group["PORCENTAJE"] = (
    df_group["CANTIDAD_CASOS"] /
    df_group.groupby("cluster")["CANTIDAD_CASOS"].transform("sum")
) * 100
df_group["PORCENTAJE"] = df_group["PORCENTAJE"].round(2)


fig = px.bar(
    df_group,
    x="cluster",
    y="CANTIDAD_CASOS",
    color=variable,
    barmode="stack",
    hover_data = "PORCENTAJE",
    title=f"Distribución de {variable} por cluster"
)

st.plotly_chart(fig, use_container_width=True)

st.warning("""
📊 **Insight clave**

**VARIABLE GENERO** :
Aunque la población total presenta una distribución equilibrada entre hombres y mujeres, 
el Grupo B está conformado exclusivamente por pacientes masculinos.

Esto indica que el modelo no está segmentando por proporción de género, sino que ha identificado 
un subconjunto específico de la población masculina con características particulares que lo diferencian claramente del resto.

Se sugiere analizar variables como diagnóstico, edad o tipo de atención para entender los factores que explican esta agrupación.
""")


############### COMPARATIVA DE EDAD ENTRE CLUSTER #######################
df_edad = df.groupby(["cluster", "RANGO_EDAD"])["CANTIDAD_CASOS"].sum().reset_index()

df_edad["PORCENTAJE"] = df_edad.groupby("cluster")["CANTIDAD_CASOS"]\
    .transform(lambda x: x / x.sum() * 100)

# Orden correcto (muy importante)
orden = ["0-5", "6-11", "12-17", "18-28", "29-59", "60+"]

df_edad["RANGO_EDAD"] = pd.Categorical(df_edad["RANGO_EDAD"], categories=orden, ordered=True)
df_edad = df_edad.sort_values("RANGO_EDAD")

df_diff = df_edad.pivot(index="RANGO_EDAD", columns="cluster", values="PORCENTAJE").reset_index()
df_diff["DIFERENCIA"] = df_diff["Grupo B"] - df_diff["Grupo A"]

################# COMPARATIVA DE REGIMEN ################

df_regimen = df.groupby(["cluster", "REGIMEN"])["CANTIDAD_CASOS"].sum().reset_index()

df_regimen["PORCENTAJE"] = df_regimen.groupby("cluster")["CANTIDAD_CASOS"]\
    .transform(lambda x: x / x.sum() * 100)


df_diff_regimen = df_regimen.pivot(index="REGIMEN", columns="cluster", values="PORCENTAJE").reset_index()
df_diff_regimen["DIFERENCIA"] = df_diff_regimen["Grupo B"] - df_diff_regimen["Grupo A"]

################### COMPARATIVA POR GRUPO DIAGNOSTICO ###########

df_grupo_dx = df.groupby(["cluster", "GRUPO_DIAGNOSTICO"])["CANTIDAD_CASOS"].sum().reset_index()

df_grupo_dx["PORCENTAJE"] = df_grupo_dx.groupby("cluster")["CANTIDAD_CASOS"]\
    .transform(lambda x: x / x.sum() * 100)


df_diff_grupo_dx = df_grupo_dx.pivot(index="GRUPO_DIAGNOSTICO", columns="cluster", values="PORCENTAJE").reset_index()
df_diff_grupo_dx["DIFERENCIA"] = df_diff_grupo_dx["Grupo B"] - df_diff_grupo_dx["Grupo A"]

################### GRAFICOS ################################

col1, col2 =st.columns(2)

with col1:
    st.markdown("### 📊 Distribución por edad")
    fig = px.bar(
    df_edad,
    x="PORCENTAJE",
    y="RANGO_EDAD",
    color="cluster",
    orientation="h",
    barmode="group",
    title="Distribución porcentual por rango de edad y cluster"
   
)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📊 Distribución por regimen")
    fig_regimen = px.bar(
    df_regimen,
    x="PORCENTAJE",
    y="REGIMEN",
    color="cluster",
    orientation="h",
    barmode="group",
    title="Distribución porcentual por regimen y cluster"
)
    st.plotly_chart(fig_regimen, use_container_width=True)

    st.markdown("### 📊 Distribución por grupo diagnostico")
    fig_grupo_dx = px.bar(
    df_grupo_dx,
    x="PORCENTAJE",
    y="GRUPO_DIAGNOSTICO",
    color="cluster",
    orientation="h",
    barmode="group",
    title="Distribución porcentual por regimen y cluster"
)
    st.plotly_chart(fig_grupo_dx, use_container_width=True)

with col2:
    st.markdown("### 📉 Diferencia entre clusters")
    fig_diff = px.bar(
    df_diff,
    x="DIFERENCIA",
    y="RANGO_EDAD",
    orientation="h",
    title="Diferencia porcentual (Grupo B - Grupo A)"
)
    st.plotly_chart(fig_diff, use_container_width=True)

    st.markdown("### 📉 Diferencia entre clusters")
    fig_diff_regimen = px.bar(
    df_diff_regimen,
    x="DIFERENCIA",
    y="REGIMEN",
    orientation="h",
    title="Diferencia porcentual (Grupo B - Grupo A)"
)
    st.plotly_chart(fig_diff_regimen, use_container_width=True)

    st.markdown("### 📉 Diferencia entre clusters")
    fig_diff_grupo_dx = px.bar(
    df_diff_grupo_dx,
    x="DIFERENCIA",
    y="GRUPO_DIAGNOSTICO",
    orientation="h",
    title="Diferencia porcentual (Grupo B - Grupo A)"
)
    st.plotly_chart(fig_diff_grupo_dx, use_container_width=True)


st.info("""
📊 **Insight clave**

**RANGO EDAD**
El Grupo A presenta una mayor concentración en población adulta (29-59) y adultos mayores (60+), 
lo que sugiere un perfil más envejecido.

Por otro lado, el Grupo B muestra una distribución más joven, con mayor participación en rangos de edad 
entre 6-11 y 18-28 años.

Este comportamiento refuerza la hipótesis de que el cluster B, compuesto exclusivamente por hombres, 
podría estar asociado a perfiles de atención más relacionados con población masculina joven.

---------------------------------------------------------------------------------------------------------

**REGIMEN**
La distribución por tipo de régimen es bastante similar entre los clusters, 
con una alta concentración en el régimen subsidiado en ambos grupos (~75%).

Esto indica que el régimen no es un factor determinante en la segmentación.

Sin embargo, se observa una mayor participación del régimen "OTRO" en el Grupo B (+4.1%), 
lo que podría estar asociado a características específicas de atención dentro de este grupo.

-----------------------------------------------------------------------------------------------------------
GRUPO DIAGNOSTICO
Se observa una mayor concentración de casos asociados a **salud mental** en ambos clusters, lo que es esperado,
siendo aún más marcada en el Grupo B (91.8%) frente al Grupo A (87.1%).

Adicionalmente, el Grupo A presenta una mayor diversidad de diagnósticos, con mayor participación 
en categorías como factores sociales, condiciones neurológicas y trastornos endocrino-metabólicos.

En contraste, el Grupo B muestra una menor dispersión clínica, concentrándose principalmente en salud mental, 
lo que sugiere un perfil más homogéneo en términos de condición de atención.
""")

st.success("""
🧠 **Conclusión – Caracterización de segmentos**

**🔵 Grupo A:**
Corresponde a un segmento poblacional más diverso, con distribución mayoritariamente compuesta por mujeres (70/30) 
y una mayor concentración en población adulta y adulta mayor. Este grupo presenta una mayor variedad 
de diagnósticos, incluyendo condiciones neurológicas, endocrinas y factores sociales, lo que sugiere 
un perfil clínico más heterogéneo.

**🔴 Grupo B:**
Se caracteriza por estar compuesto exclusivamente por pacientes masculinos, con una mayor concentración 
en población joven. Este grupo presenta una alta predominancia de diagnósticos asociados a salud mental (91.8%), 
con menor diversidad en otras condiciones, lo que indica un perfil más específico y homogéneo.

**🎯 Conclusión general:**
El modelo identifica un segmento claramente diferenciado compuesto por hombres jóvenes con alta prevalencia 
de condiciones relacionadas con salud mental, lo que podría representar una población objetivo para estrategias 
específicas de atención, prevención e intervención dentro del sistema de salud.
""")






