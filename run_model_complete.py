import subprocess
import os
import sys
import time

def run_script(script_name):
    """Ejecuta un script de Python y maneja errores."""
    script_path = os.path.join("pipeline", script_name)
    
    print(f"\n{'='*50}")
    print(f"🚀 EJECUTANDO: {script_name}")
    print(f"{'='*50}")
    
    start_time = time.time()
    
    # Ejecutamos el script usando el mismo intérprete de Python actual
    result = subprocess.run([sys.executable, script_path], capture_output=False, text=True)
    
    end_time = time.time()
    duration = end_time - start_time
    
    if result.returncode == 0:
        print(f"✅ {script_name} finalizado con éxito en {duration:.2f} segundos.")
        return True
    else:
        print(f"❌ ERROR en {script_name}. El proceso se ha detenido.")
        return False

def main():
    # El orden lógico de dependencia para el proyecto del hospital
    pipeline_flow = [
        "pipeline_ETL.py",       # 1. Limpieza y carga inicial
        "pipeline_prep.py",      # 2. Preprocesamiento + PCA (genera 41 componentes)
        "pipeline_modeling.py",  # 3. Entrenamiento (busca el mejor entre KMeans/AC/GMM)
        "pipeline_inference.py"  # 4. Asignación final de clusters a la data limpia
    ]

    print("--- INICIANDO PIPELINE COMPLETO DEL HOSPITAL ---")
    
    total_start = time.time()
    
    for script in pipeline_flow:
        success = run_script(script)
        if not success:
            sys.exit(1) # Detener todo si un paso falla
            
    total_duration = time.time() - total_start
    print(f"\n{'*'*50}")
    print(f"🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
    print(f"Tiempo total de ejecución: {total_duration/60:.2f} minutos")
    print(f"{'*'*50}")

if __name__ == "__main__":
    main()