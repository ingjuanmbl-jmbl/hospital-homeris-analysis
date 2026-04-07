# 🏥 Health Analytics Platform - Hospital Homeris

> **Análisis de segmentación fenotípica y caracterización de pacientes mediante aprendizaje no supervisado.**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg?style=flat-square&logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E.svg?style=flat-square&logo=scikit-learn)
![Status](https://img.shields.io/badge/Status-Research--In--Progress-green.svg?style=flat-square)

Esta plataforma integra técnicas de **Machine Learning No Supervisado** para identificar patrones ocultos en datos hospitalarios, permitiendo una transición de una gestión reactiva a una caracterización proactiva de la población atendida.


---

## 🎯 Objetivo del Proyecto

Desarrollar un ecosistema analítico que permita la **segmentación multidimensional de pacientes**, facilitando la identificación de clústeres clínicos y demográficos para optimizar la asignación de recursos y el diseño de programas de intervención en salud.

---
## 🔬 Arquitectura y Metodología

El proyecto sigue un enfoque modular basado en **Principios de Ingeniería de Software** aplicado a la Ciencia de Datos:

1.  **Ingeniería de Características & PCA:** Implementación de pipelines de preprocesamiento robustos, incluyendo codificación de variables categóricas clínicas y **Reducción de Dimensionalidad (PCA)** para mitigar el ruido y la redundancia de los datos.
2.  **Clustering Avanzado:** Aplicación de algoritmos de agrupación (K-Means / Hierarchical) validados mediante métricas de cohesión y separación (**Coeficiente de Silueta**)
3.  **Visualización Científica:** Dashboard interactivo desarrollado en Streamlit con visualizaciones dinámicas (Plotly) para la interpretación de componentes principales y perfiles de segmento.

---

## 🚀 Funcionalidades

### 📈 Análisis Descriptivo
- Exploración de datos iniciales principalmente basado en:
  - Género
  - Edad
  - Régimen
  - Diagnóstico

### 🔍 Clustering (Machine Learning)
- Segmentación de pacientes mediante algoritmos no supervisados y reducción de la dimensionalidad (PCA)
- Identificación de grupos homogéneos

### 👥 Caracterización de Pacientes
- Análisis detallado de cada cluster:
  - Perfil demográfico
  - Diagnóstico predominante
  - Diferencias entre grupos

### ⚙️ Pipeline Maestro
- Ejecución completa del flujo:
  - ETL
  - Preparación de datos
  - Modelado
  - Inferencia

---

## 🧠 Principales Hallazgos

- Identificación de un segmento compuesto por **hombres jóvenes con alta concentración en salud mental**
- Identificación de un segmento más diverso compuesto mayoritariamente por **mujeres adultas**
- Evidencia de diferencias significativas en edad y perfil clínico entre clusters

---

## 🛠️ Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- Scikit-learn
- Plotly

---


## 📂 Estructura del Proyecto

```text

├── .venv/                      # Entorno virtual de Python
├── artifacts/                  # Objetos generados (binarios)
│   ├── models/                 # Modelos entrenados (.joblib)
│   └── preprocessors/          # Encoders, scalers y transformadores
├── data/                       # Almacenamiento de datos (no versionado)
│   ├── raw/                    # Datos originales sin procesar
│   ├── preprocessed/           # Datos tras limpieza inicial
│   ├── PCA/                    # Datos con reducción de dimensionalidad
│   ├── clean/                  # Datos finales listos para modelado
│   └── best_model_result/      # Resultados y métricas del mejor modelo
├── notebooks/                  # Experimentos y análisis exploratorio
│   ├── 01_ETL.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_preprocessing.ipynb
│   ├── 04_modeling.ipynb
│   ├── 05_inference.ipynb
│   ├── 06_analisis_resultados.ipynb
│   └── 07_Segmento.ipynb
├── pages/                      # Vistas para la aplicación de Streamlit
│   ├── 1_Analisis_Descriptivo.py
│   ├── 2_Analisis_no_Supervisado.py
│   └── 3_Caracterización_de_pacientes.py
├── pipeline/                   # Scripts de automatización del flujo
│   ├── pipeline_ETL.py
│   ├── pipeline_prep.py
│   ├── pipeline_modeling.py
│   └── pipeline_inference.py
├── src/                        # Código fuente modular (funciones core)
│   ├── extraction.py           # Conexión y extracción de datos
│   ├── cleaning.py             # Funciones de limpieza
│   ├── preprocessing.py        # Transformación de variables
│   ├── PCA.py                  # Lógica de reducción de componentes
│   ├── modeling.py             # Definición de arquitecturas de modelos
│   └── utils.py                # Funciones auxiliares y herramientas
├── .gitignore                  # Archivos y carpetas excluidos de Git
├── Home.py                     # Punto de entrada principal (Streamlit)
├── LICENSE                     # Términos de uso del proyecto
├── README.md                   # Documentación del proyecto
├── requirements.txt            # Dependencias del sistema
└── run_model_complete.py       # Script de ejecución integral

## ⚠️ Uso del proyecto

Este proyecto ha sido desarrollado con fines educativos/investigativos y de portafolio.

Se permite su visualización y referencia, pero:

- ❌ No está permitido su uso comercial  
- ❌ No está permitido modificarlo o redistribuir versiones derivadas  
- ❌ No está permitido utilizar el código como base para otros proyectos sin autorización  

Este proyecto se encuentra bajo la licencia:

**Creative Commons BY-NC-ND 4.0**

Para más información, consultar el archivo `LICENSE`.

## ✉️ Contacto e Investigación
Si tienes dudas sobre la metodología aplicada o estás interesado en colaborar en proyectos de analítica en salud, no dudes en contactarme:
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Juan_Manuel_Betancur-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/ingjuanmbl/)
[![Email](https://img.shields.io/badge/Email-ing.juanmbl@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ing.juanmbl@gmail.com)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Chat-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/573128747344)
