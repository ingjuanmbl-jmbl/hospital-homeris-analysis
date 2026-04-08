from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de la página
st.set_page_config(
    page_title="Homeris Data Dashboard",
    layout="wide",
    page_icon="🏥")

st.title("🧑‍⚕️ Análisis Descriptivo - E.S.E Hospital Mental Homeris")
st.info("""
Este módulo tiene como objetivo realizar una **radiografía situacional** de las atenciones en HOMERIS. 
A través de la exploración de variables demográficas y clínicas, identificamos tendencias de volumen, 
distribución geográfica y picos de atención que sirven como línea base para la toma de decisiones 
operativas y la asignación de personal médico.
""")

#Carga del data set
@st.cache_data
def cargar_datos():
    base_path = Path(__file__).resolve().parent
    data_path = base_path / "../data/clean/homeris-data-clean.csv"
    
    df = pd.read_csv(data_path)
    return df

df = cargar_datos()

#Asignación de filtros
with st.sidebar:
    st.title("📥 Parámetros de análisis")

    #Asignación de parametros de analisis (Filtros)

    #filtro por añ0
    anio = st.multiselect(
        "Filtrar por año",
        options=df['ANIO'].unique(),
        default=df['ANIO'].unique(),
    )

    #filtro por regimen
    regimen = st.multiselect(
        "Filtrar por regimen",
        options=df['REGIMEN'].unique(),
        default=df['REGIMEN'].unique(),
    )

    #filtro por rango de edad
    rango_edad = st.multiselect(
        "Filtrar por rango de edad",
        options=df['RANGO_EDAD'].unique(),
        default=df['RANGO_EDAD'].unique(),
    )

    grupo_diagnostico = st.multiselect(
        "Filtrar por rango de grupo diagnostico",
        options=df['GRUPO_DIAGNOSTICO'].unique(),
        default=df['GRUPO_DIAGNOSTICO'].unique(),
    )

    tipo_diagnostico = st.multiselect(
        "Filtrar por tipo de diagnostico",
        options= df['SALUD_MENTAL_CLASS'].unique(),
        default=df['SALUD_MENTAL_CLASS'].unique()
    )

#Aplicar Filtros

df_filtrado = df[
    (df['ANIO'].isin(anio)) &
    (df['REGIMEN'].isin(regimen)) &
    (df['RANGO_EDAD'].isin(rango_edad)) &
    (df['GRUPO_DIAGNOSTICO'].isin(grupo_diagnostico)) &
    (df['SALUD_MENTAL_CLASS'].isin(tipo_diagnostico))
]

#Metricas Clave

st.subheader("Métricas Generales")
st.markdown("---")

col1, col2, col3 =st.columns(3)

with col1:
    st.metric(
        label = "Total Atenciones regitradas",
        value = f"{df_filtrado['CANTIDAD_CASOS'].sum():,.0f}"
    )

with col2:

    top_diagnostico = (
        df_filtrado.groupby('DIAGNOSTICO')['CANTIDAD_CASOS']
        .sum().idxmax()
    )
    st.markdown("### Diagnóstico más recurrente")
    st.info(top_diagnostico)


with col3:

    top_grupo = (
        df_filtrado.groupby('GRUPO_DIAGNOSTICO')['CANTIDAD_CASOS']
        .sum().idxmax()
    )
    st.markdown("### Grupo Diagnóstico más recurrente")
    st.info(top_grupo)
st.markdown("---")

st.subheader("Tendencia por mes de casos registrados",)

#Grafico general de la tendendencia
#Agrupamos 
df_group_period = df_filtrado.groupby("PERIODO_MENSUAL")["CANTIDAD_CASOS"].sum().reset_index()

#Graficamos
fig_period = px.line(
    df_group_period,
    x="PERIODO_MENSUAL",
    y="CANTIDAD_CASOS",
    title="¿Cúal es la tendencia de casos atendidos en el hospital?",
    markers=True
)

fig_period.update_traces(
    line_shape="spline", #Curva suave
    text=df_group_period["CANTIDAD_CASOS"]
)

fig_period.update_layout(
    paper_bgcolor="#f5f7fa",   # fondo externo
    plot_bgcolor="#f5f7fa"     # fondo interno
    )

st.plotly_chart(fig_period, use_container_width=True)

#Analisis Clave
with st.expander("🔎 Ver análisis"):
    st.info("""
    - 📉 En **marzo** se registra el punto más bajo de atención.  
    - 📈 A partir de abril se evidencia una **tendencia creciente marcada**, con picos en **julio y octubre**, siendo este último el valor más alto.  
    - 🔄 Se evidencian **fluctuaciones mensuales**, asociadas a factores estacionales o epidemiológicos.  
    - 📉 En noviembre se observa una **disminución posterior al pico**, indicando estabilización.  

    ### Insight clave
    El **segundo semestre concentra mayor volumen de pacientes atendidos**, lo que sugiere reforzar capacidad operativa y recursos clínicos.
    """)

st.markdown("---")

#Graficos de diagnostico
st.subheader("Análisis por Diagnostico")
col_izq, col_der = st.columns(2)

with col_izq:
    df_group_salud_mental = (
        df_filtrado.groupby("SALUD_MENTAL_CLASS")["CANTIDAD_CASOS"]
        .sum().reset_index()
        )

    fig_group_salud_mental = px.pie(
        df_group_salud_mental,
        values="CANTIDAD_CASOS",
        names="SALUD_MENTAL_CLASS",
        title="Proporción de Casos atendidos<br>Salud Mental vs Otros Diagnósticos",
        width=400,
        height=400
    )

    fig_group_salud_mental.update_layout(
    paper_bgcolor="#f5f7fa",   # fondo externo
    plot_bgcolor="#f5f7fa"     # fondo interno
    )

    st.plotly_chart(fig_group_salud_mental, use_container_width=True)

with col_der:
    fig_g_dx_top = px.treemap(
    df_filtrado,
    path=["GRUPO_DIAGNOSTICO","DIAGNOSTICO"],
    values="CANTIDAD_CASOS",
    title="Proporción de casos por grupo diagnóstico",
    height=1000,   # más alto
    width=1000     # menos ancho
    )

    fig_g_dx_top.update_layout(
    paper_bgcolor="#f5f7fa",   # fondo externo
    plot_bgcolor="#f5f7fa"     # fondo interno
    )

    st.plotly_chart(fig_g_dx_top, use_container_width=True)



with col_izq:
    st.info(
        """
        ### 💡 Insight Clave
        - Aunque la atención en salud mental representa la mayoría de los casos (88.5%), 
        se identifica que un 11.5% de las atenciones corresponde a diagnósticos no relacionados, 
        lo que evidencia la existencia de una demanda adicional de servicios generales dentro del
        hospital.

        A la vez, dentro del 11,5% los diagnosticos más recurrentes se concentran en el grupo de
         FACTORES SOCIALES (987/4003)como por ejemplo:
        * PROBLEMAS RELACIONADOS CON EL AMBIENTE SOCIAL
        * PROBLEMAS RELACIONADOS CON EL GRUPO PRIMARIO DE APOYO

        El segundo Grupo esta relacionado con SINTOMAS Generales (837/4003) donde se destacan los siguientes diagnosticos:
        * DOLOR NO CLASIFICADO EN OTRA PARTE
        * OTROS SINTOMAS Y SIGNOS QUE INVOLUCRAN LA FUNCION COGNOSCITIVA Y LA CONCIENCIA
        """
    )

#Graficos de diagnostico
st.subheader("Análisis por Aspectos Sociodemograficos del paciente")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    df_genero  = (
        df_filtrado.groupby('GENERO')['CANTIDAD_CASOS']
        .sum()
        .reset_index()
        )
    fig_genero = px.pie(
        df_genero,
        names='GENERO',
        values='CANTIDAD_CASOS',
        title= "Distribución de casos por genero"
    )

    fig_genero.update_layout(
    paper_bgcolor="#f5f7fa",   # fondo externo
    plot_bgcolor="#f5f7fa"     # fondo interno
    )
    st.plotly_chart(fig_genero, use_container_width=True)
    
    st.info(
    """
    💡
    La distribución de casos por género es equilibrada,
    con una ligera predominancia del masculino (50.6%)
    frente al femenino (49.4%).
    """
    )

with col2:
    df_regimen = (
        df_filtrado.groupby("REGIMEN")["CANTIDAD_CASOS"]
        .sum()
        .reset_index()
        .sort_values("CANTIDAD_CASOS", ascending=True)
        )

    fig_regimen = px.bar(
        df_regimen,
        x="CANTIDAD_CASOS",
        y="REGIMEN",
        orientation="h",
        text="CANTIDAD_CASOS",
        title="Casos por régimen de afiliación"
    )

    fig_regimen.update_layout(
    paper_bgcolor="#f5f7fa",   # fondo externo
    plot_bgcolor="#f5f7fa"     # fondo interno
    )

    st.plotly_chart(fig_regimen, use_container_width=True)
   
    st.info(
    """
    💡
    El Régimen Subsidiado concentra la gran mayoría de los casos analizados
    con 26,449 registros, una cifra que triplica ampliamente
    al Régimen Contributivo (6,782). Esta brecha sugiere que la población atendida 
    o afectada pertenece mayoritariamente a sectores vulnerables, lo que implica
    que cualquier estrategia de intervención o asignación de recursos debe priorizar 
    la red de servicios y programas enfocados en este grupo.
    """
    )


df_edad = (
    df_filtrado.groupby("RANGO_EDAD")["CANTIDAD_CASOS"]
        .sum()
        .reset_index()
        )

# Orden correcto (muy importante)
orden = ["0-5", "6-11", "12-17", "18-28", "29-59", "60+"]

df_edad["RANGO_EDAD"] = pd.Categorical(df_edad["RANGO_EDAD"], categories=orden, ordered=True)
df_edad = df_edad.sort_values("RANGO_EDAD")

fig_edad = px.bar(
    df_edad,
    x="CANTIDAD_CASOS",
    y="RANGO_EDAD",
    orientation="h",
    text="CANTIDAD_CASOS",
    title="Distribución de casos por rango de edad"
)

fig_edad.update_traces(
    textposition="outside",
    texttemplate="%{text:,}"
)

fig_edad.update_layout(
    paper_bgcolor="#f5f7fa",   # fondo externo
    plot_bgcolor="#f5f7fa"     # fondo interno
)

st.plotly_chart(fig_edad, use_container_width=True)

st.info(
    """
    💡
    La mayor presión asistencial del hospital se concentra en la población adulta (29-59 años), 
    que aporta 14,208 atenciones.

    * Dato Clave: El volumen de este grupo supera la suma de los tres rangos de edad más 
    jóvenes (0-28 años), lo que define la especialidad de recursos que el hospital debe priorizar.

    El hospital atiende primordialmente a una población adulta
    en condiciones socioeconómicas vulnerables (Régimen Subsidiado).
    Existe una oportunidad de optimizar procesos de facturación hacia
    el régimen subsidiado para asegurar el flujo de recursos,
    dado que este sostiene más de 3/4 partes de la operación hospitalaria.
    """
    )
        
    


    


