
import streamlit as st
import sys
import os
import pandas as pd
from run_model_complete import main as ejecutar_orquestador_completo
import time

#Configurar rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)



#Importar pipelines
from pipeline import pipeline_modeling
from pipeline.pipeline_ETL import pipeline_clean
from pipeline.pipeline_prep import pipeline_prep
from pipeline.pipeline_modeling import pipe_line_modeling
from pipeline.pipeline_inference import pipeline_inference


st.set_page_config(page_title="Hospital-homeris-analysis", layout="wide")
st.markdown("""
    <h1 style='margin-bottom:0;'>🏥 Análisis Avanzado de Agrupamiento y Reducción de Dimensionalidad para la Caracterización del Paciente en Salud Mental</h1>
    <p style='color:gray; margin-top:0; font-size:18px;'>
    Plataforma de inteligencia de datos que integra algoritmos de aprendizaje no supervisado y técnicas de reducción de dimensionalidad
    para la identificación de fenotipos demográficos y patrones de demanda asistencial, optimizando la gestión de recursos y la intervención
    personalizada en servicios de salud mental.
    </p>
""", unsafe_allow_html=True)

st.markdown("""
### 🎯 Objetivo

Modelar la estructura de la demanda asistencial mediante técnicas de agrupación avanzada para caracterizar fenotipos de pacientes,
permitiendo la extracción de evidencia estadística que fundamente la toma de decisiones clínicas y la optimización estratégica
de los servicios hospitalarios
""")


st.markdown("<hr style='border:1px solid #eee;'>", unsafe_allow_html=True)


def card(title, description, button_text, page):
    st.markdown(f"""
        <div style="
            background-color:#ffffff;
            padding:20px;
            border-radius:12px;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
            height:220px;
        ">
            <h3>{title}</h3>
            <p style='color:gray;'>{description}</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button(button_text, key=title):
        st.switch_page(page)    

# =============================
# 📊 MÓDULOS PRINCIPALES
# =============================

st.markdown("#### 📊 Módulos de análisis")

col1, col2, col3 = st.columns(3)

with col1:
    card(
        "📈 Análisis Descriptivo",
        "Explora la distribución de casos por variables demográficas y clínicas.",
        "Explorar",
        "pages/1_Analisis_Descriptivo.py"
    )

with col2:
    card(
        "🔍 Clustering",
        "Segmentación de pacientes mediante modelos de Machine Learning no supervisado.",
        "Explorar",
        "pages/2_Analisis_no_Supervisado.py"
    )

with col3:
    card(
        "👥 Caracterización de Pacientes",
        "Análisis detallado de los clusters identificados y sus diferencias.",
        "Explorar",
        "pages/3_Caracterización_de_pacientes.py"
    )


# =============================
# ⚙️ PIPELINE MAESTRO
# =============================

st.markdown("---")
st.markdown("### ⚙️ Ejecución del modelo")

st.warning("""
Este módulo ejecuta el flujo completo de analítica:
**ETL → Preparación → Modelado → Inferencia**
""")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="
        background-color:#f8f9fa;
        padding:20px;
        border-radius:12px;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
    ">
        <h3>🔄 Pipeline Maestro</h3>
        <p style='color:gray;'>
        Ejecuta todo el proceso de analítica de manera automática, 
        actualizando los resultados del modelo y la segmentación de pacientes.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    ejecutar = st.button("🚀 Ejecutar pipeline", use_container_width=True)


# =============================
# 🚀 EJECUCIÓN DEL PIPELINE
# =============================

if ejecutar:
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        start_time = time.time()
        
        status_text.info("⏳ Ejecutando pipeline completo... Por favor espera.")
        progress_bar.progress(20)
        
        ejecutar_orquestador_completo()
        
        progress_bar.progress(100)
        end_time = time.time()
        
        st.success(f"""
        ✅ Pipeline ejecutado correctamente  
        ⏱ Tiempo total: {round(end_time - start_time, 2)} segundos
        """)

        if st.button("🔄 Refrescar datos"):
            st.rerun()

    except Exception as e:
        st.error(f"❌ Error en la ejecución del pipeline: {e}")
