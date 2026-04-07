from sklearn.decomposition import PCA
import pandas as pd
def aplicar_PCA(df_pp: pd.DataFrame, n_components=0.95, random_state=42):
    """
    Entrena y aplica PCA  a un Dataset previamente preprocesado.
        Args:
            df_pp: Data previamente preprocesada y scalados
            n_componets: Varianza total a conservar (0.95 = 95%) o número fijo de componentes.
            random_state: Semilla para reproducibilidad.
        Returns:
            df_pca: DataFrame con los componentes principales.
            pca_model: El objeto PCA entrenado.
    """

    #Inicialización del modelo PCA
    pca_model = PCA(n_components=n_components, random_state=random_state)

    #Ajustar y transformar
    # Ajustar y transformar
    pca_data = pca_model.fit_transform(df_pp)

    # Crear nombres de columnas dinámicos (PC1, PC2, ...)
    cols = [f'PC{i+1}' for i in range(pca_data.shape[1])]

    # Convertir a DataFrame manteniendo el índice original
    df_pca = pd.DataFrame(pca_data, columns=cols, index=df_pp.index)

    print(f"--- Resumen PCA ---")
    print(f"Componentes generados: {pca_model.n_components_}")
    print(f"Varianza total explicada: {pca_model.explained_variance_ratio_.sum():.2%}")
    
    return df_pca, pca_model
