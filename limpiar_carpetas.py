import os
import shutil

# Carpeta base que contiene todas las subcarpetas de instrumentos
CARPETA_RAIZ = "partituras_ordenadas"

def vaciar_contenido_de_subcarpetas(ruta_base):
    if not os.path.exists(ruta_base):
        print(f"[CREADO] La carpeta raíz '{ruta_base}' no existía. Se ha creado.")
        os.makedirs(ruta_base)
        return

    for nombre_carpeta in os.listdir(ruta_base):
        ruta_carpeta = os.path.join(ruta_base, nombre_carpeta)
        if os.path.isdir(ruta_carpeta):
            for archivo in os.listdir(ruta_carpeta):
                ruta_archivo = os.path.join(ruta_carpeta, archivo)
                if os.path.isfile(ruta_archivo) or os.path.islink(ruta_archivo):
                    os.unlink(ruta_archivo)
                elif os.path.isdir(ruta_archivo):
                    shutil.rmtree(ruta_archivo)
            print(f"[OK] Vacío '{nombre_carpeta}'")
    print("\n[INFO] Limpieza de subcarpetas completada.")

# Ejecutar limpieza
vaciar_contenido_de_subcarpetas(CARPETA_RAIZ)
