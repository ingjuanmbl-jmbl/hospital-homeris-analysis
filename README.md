# 🏥 Health Analytics Platform - Hospital Homeris

> **Análisis de segmentación fenotípica y caracterización de pacientes mediante aprendizaje no supervisado.**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg?style=flat-square&logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E.svg?style=flat-square&logo=scikit-learn)
![Status](https://img.shields.io/badge/Status-Research--In--Progress-green.svg?style=flat-square)

Esta plataforma integra técnicas de **Machine Learning No Supervisado** para identificar patrones ocultos en datos hospitalarios, permitiendo una transición de una gestión reactiva a una caracterización proactiva de la población atendida.

---

## 📊 Origen de los Datos y Contexto del Problema

Este proyecto aborda un **problema real de salud pública** utilizando datos oficiales del departamento de Risaralda, Colombia. 

Los datos provienen del **Registro de Casos de Atención del Hospital Mental Universitario de Risaralda (HOMERIS)**, disponibles en el portal de Datos Abiertos de Colombia:
* **Fuente:** [Datos.gov.co - Casos de Atención HOMERIS](https://www.datos.gov.co/Salud-y-Protecci-n-Social/REGISTRO-DE-CASOS-DE-ATENCION-HOMERIS-RISARALDA/izfv-6qvv/about_data)

### El Desafío Real
La gestión de servicios en salud mental requiere una comprensión profunda de la demanda. Este proyecto utiliza técnicas de **Machine Learning No Supervisado** para segmentar a la población atendida, permitiendo identificar perfiles críticos de pacientes. El objetivo es transformar datos administrativos en información accionable que permita optimizar recursos hospitalarios y diseñar programas de intervención focalizados según el género, la edad y el diagnóstico.

---
## 🌐 Acceso a la Plataforma en Vivo
Puedes interactuar con los modelos y explorar los clústeres en tiempo real aquí:
🚀 **[Hospital Homeris Analytics - Demo en la Nube](https://hospital-homeris-analysis-5e3mu8p9ypcsprptu4abtx.streamlit.app/)**


---

## 🎯 Objetivo del Proyecto

Modelar la estructura de la demanda asistencial mediante **técnicas de agrupación avanzada** para caracterizar fenotipos de pacientes,
permitiendo la extracción de evidencia estadística que fundamente la toma de decisiones clínicas y la optimización estratégica
de los servicios hospitalarios

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

## 🧠 Principales Hallazgos y Caracterización

A través de la reducción de dimensionalidad (**PCA**) conservando el 70% de la varianza y algoritmos de clustering, se identificaron dos perfiles de pacientes con comportamientos epidemiológicos claramente diferenciados:

### 1. Segmento de Riesgo Joven Masculino (30% de la población)
* **Perfil:** Exclusivamente hombres en rango de edad joven.
* **Hallazgo:** Presentan la mayor concentración de diagnósticos críticos de salud mental. Este grupo muestra un comportamiento "especializado", sugiriendo que acceden al sistema principalmente ante crisis o patologías agudas, con menor incidencia en consultas preventivas.
* **Impacto:** Identifica una oportunidad crítica para diseñar programas de captación temprana y prevención enfocados específicamente en la población masculina joven.

### 2. Segmento de Gestión Integral Adulta (70% de la población)
* **Perfil:** Composición diversa con fuerte predominio femenino (70%) y población adulta.
* **Hallazgo:** Es el segmento de mayor volumen y variedad diagnóstica. La presencia mayoritaria de mujeres sugiere que este grupo constituye el núcleo de la demanda recurrente, abarcando un espectro clínico más amplio que va desde el control administrativo hasta el seguimiento crónico.
* **Impacto:** Representa la base operativa principal del hospital, donde la eficiencia en la asignación de citas y la continuidad del tratamiento son los mayores pilares de gestión.

### 🧪 Nota Técnica sobre el Modelo
Para lograr esta segmentación, se aplicó un **Análisis de Componentes Principales (PCA)**. Se determinó que el **género y la etapa del ciclo vital** son los predictores más robustos de la ruta de atención en HOMERIS. La elección de un modelo de 2 clústeres responde al aseguramiento para que los grupos sean interpretables y accionables para el negocio.

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

```

---
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
