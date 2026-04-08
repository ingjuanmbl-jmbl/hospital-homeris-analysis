import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Configuración de la página
st.set_page_config(
    page_title="Analisis no supervisado",
    layout="wide",
    page_icon="🔍")

st.title("🔍 Analisis No Supervisado - Clustering")
st.info(
    """
    El propósito del análisis no sueprvisado es **descubrir patrones ocultos** en la población de pacientes que no son 
    visibles a simple vista. Mediante algoritmos de agrupación (Clustering) y reducción de dimensionalidad (PCA), 
    segmentamos a los pacientes en grupos con comportamientos clínicos y demográficos similares. Esto permite 
    pasar de una atención genérica a una **estrategia de salud dirigida y personalizada**.
    """
)


st.markdown("<h4 style='text-align: center;'>Metricas de ajuste</h4>", unsafe_allow_html=True)
st.markdown("---")


#Cargar dataset de metricas

# Esto asegura que 'src' sea visible sin importar desde dónde se ejecute el script

#Aasignamos rutas de lectura
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
path_input_result = os.path.join(BASE_DIR,"data","best_model_result", "best_model_result.csv")
path_input_pca = os.path.join(BASE_DIR,"data","PCA","homeris-data-clean-preprocessed-PCA.csv")



########################### CARGAR DATA SET CON METRICAS FINALES #######################################

@st.cache_data

def cargar_resultados():

    df = pd.read_csv(path_input_result)
    #Ajustamos el nombre de los mdodelos
    mapeo_modelos = {
        'kmeans': 'K-Means Clustering',
        'ac': 'Agglomerative Clustering',
        'gmm': 'Gaussian Mixture Models'
    }
    # Esto reemplaza los valores en la columna actual
    df['modelo'] = df['modelo'].map(mapeo_modelos)

    return df

df = cargar_resultados()

########################## ASIGNACION DE VARIABLES DE METRICAS GLOBALES DEL MEJOR MODELO ##############################################################

# 1. Localizar la fila completa con el Silhouette Score más alto
fila_mejor_modelo = df.loc[df['silhouette'].idxmax()]

# 2. Asignar los valores a variables individuales para los KPI
mejor_modelo_nombre = fila_mejor_modelo['modelo']
mejor_k = fila_mejor_modelo['k']

mejor_score = f"{fila_mejor_modelo['silhouette']:,.3f}"

##### ASIGNACIÓN DE FILTROS ###############

with st.sidebar:
    st.title("Parametros de entrada")

    modelo = st.multiselect(
        "Filtrar por modelo",
        options=df['modelo'].unique(),
        default = fila_mejor_modelo['modelo']
    )

#Df filtrado

df_filtrado = df[
    (df['modelo'].isin(modelo))
]
######### METRICAS GLOBALES ############

col1, col2, col3 = st.columns(3)

with col1:
    st.write("Mejor Modelo Encontrado:")
    st.info(f"🏆 {mejor_modelo_nombre}")

with col2:
    st.metric(
        label = "Mejor K Encontrado",
        value = mejor_k
    )

with col3:
    st.metric(
        label = "Mejor Silhouette",
        value = mejor_score
    )



st.markdown("---")

c1, c2 = st.columns(2)

with c1:
    fig_silhouette = px.line(
    df_filtrado,
    x="k",
    y="silhouette",
    markers=True,
    template="plotly_white",
    labels={"k": "Número de Grupos (k)", "silhouette": "Puntaje de Silueta"},
    title="Comportamiento indicador de silueta para cada grupo"
)



    fig_silhouette.update_layout(
        title_x=0, # Centra el título
        hovermode="x unified", # Muestra el valor al pasar el mouse sobre el eje X
        yaxis_range=[0, df_filtrado['silhouette'].max() + 0.1] # Ajusta el eje Y para ver mejor la escala
    )
    st.plotly_chart(fig_silhouette, use_container_width=True)


with c2:
        fig_ig_calinski_harabasz = px.line(
        df_filtrado,
        x="k",
        y="calinski_harabasz",
        markers=True,
        template="plotly_white",
        labels={"k": "Número de Grupos (k)", "silhouette": "Puntaje de calinski_harabasz"},
        title="Comportamiento indicador de calinski_harabasz para cada grupo"
)



        fig_ig_calinski_harabasz.update_layout(
            title_x=0, # Centra el título
            hovermode="x unified", # Muestra el valor al pasar el mouse sobre el eje X
            yaxis_range=[0, df_filtrado['calinski_harabasz'].max() + 0] # Ajusta el eje Y para ver mejor la escala
        )
        st.plotly_chart(fig_ig_calinski_harabasz, use_container_width=True)

st.info(
    """
    ### 💡 Interpretación de la Segmentación: Estructura Óptima de Datos

    Tras evaluar configuraciones desde **$k=2$ hasta $k=10$**, el motor de optimización determinó que el K optimo es K=10;
    Sin embargo al realizar la asignación de cada grupo el algoritmo determina que de fondo solo existe una **división binaria**.

    * **Consolidación de Perfiles:** Aunque el espacio de búsqueda fue amplio, las métricas de **Silueta y Calinski-Harabasz** alcanzan su punto máximo de estabilidad con dos grupos. Esto indica que la densidad de los datos hospitalarios tiende naturalmente a concentrarse en dos nodos principales de comportamiento (identificados técnicamente como los índices 2 y 9).
    
    * **Robustez Estadística:** La tendencia decreciente en los indicadores al intentar forzar más clústeres sugiere que añadir segmentos adicionales solo generaría "ruido" y diluiría la interpretabilidad. Al mantener una partición en dos grandes perfiles (**Grupo A y Grupo B**), garantizamos una estrategia clínica y administrativa clara, accionable y libre de sobreajuste (*overfitting*).

    **Conclusión:** Esta segmentación binaria es la representación más fiel de la realidad operativa, permitiendo al hospital diferenciar sus protocolos de atención sin atomizar innecesariamente sus recursos.
    """
)   


st.markdown("---")

@st.cache_data

def cargar_data_pca():
    df_pca = pd.read_csv(path_input_pca)
    return  df_pca  

df_pca = cargar_data_pca ()

# Título de la sección
st.header("Análisis de Densidad Poblacional (PCA)")

# Crear el gráfico de dispersión
fig = px.scatter(
    df_pca, 
    x='PC1', 
    y='PC2',
    title="Visualización del Espacio Latente (PC1 vs PC2)",
    labels={'PC1': 'Componente Principal 1', 'PC2': 'Componente Principal 2'},
    template="plotly_white",
    opacity=0.4, # Transparencia para ver la acumulación de puntos
    color_discrete_sequence=['#007bff'] 
)

# Ajustes estéticos
fig.update_traces(marker=dict(size=4))
fig.update_layout(
    xaxis_title="Eje de Mayor Varianza",
    yaxis_title="Eje de Segunda Varianza",
    hovermode="closest"
)

# Renderizar en la App
st.plotly_chart(fig, use_container_width=True)

# --- INTERPRETACIÓN TÉCNICA EN ST.INFO ---
st.info(f"""
### **Interpretación Técnica: Estructura de Densidad y Segmentación Óptima**

Al observar la dispersión en el espacio latente, se identifican patrones de "islas" simétricas que, tras un análisis exhaustivo, revelan la configuración más robusta para el Hospital:

1. **Efecto de Variables Categóricas (Grid Effect):**
   Las agrupaciones visibles son **coordenadas de categorías binarias** (ej. Género o Régimen). Sin embargo, el modelo ha logrado identificar que, dentro de esta rejilla, la población se polariza en dos grandes comportamientos estadísticos, representados por los clústeres identificados (Grupo A y Grupo B).

2. **Consolidación de Perfiles (2 y 9):**
   Aunque el algoritmo evaluó hasta 10 posibles grupos, la densidad de los datos forzó una convergencia natural hacia estos dos nodos principales. Esto indica que cualquier intento de sub-segmentación adicional (k > 2) carecería de diferenciación clínica real y solo generaría ruido estadístico.



**Conclusión para la Gestión Hospitalaria:**
El análisis valida que el hospital atiende a una población con dos perfiles de atención claramente definidos. Se recomienda enfocar los recursos en optimizar las rutas asistenciales para estos dos grandes bloques, en lugar de dispersar esfuerzos en múltiples micro-segmentos sin sustento estadístico.
""")

