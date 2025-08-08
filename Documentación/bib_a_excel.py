import bibtexparser
import pandas as pd
import os

# --- CONFIGURACIÓN ---
# Ruta completa de tu archivo de bibliografía BibTeX.
# IMPORTANTE: Python usa diagonales normales '/' o dobles diagonales inversas '\\'.
ruta_bib = r"D:\OneDrive\Facultad de Química\Titulación\jr-tesis\referencias.bib"

# --- LÓGICA DEL SCRIPT (NO NECESITAS MODIFICAR ABAJO DE ESTA LÍNEA) ---

# Define la ruta del archivo de salida de Excel en el mismo directorio.
directorio = os.path.dirname(ruta_bib)
nombre_archivo_excel = os.path.splitext(os.path.basename(ruta_bib))[0] + ".xlsx"
ruta_excel = os.path.join(directorio, nombre_archivo_excel)

print(f"Iniciando la lectura del archivo: {ruta_bib}")

try:
    # Abre y lee el archivo .bib con el parser
    with open(ruta_bib, 'r', encoding='utf-8') as bibtex_file:
        # Usamos un parser permisivo para evitar errores con formatos no estándar
        parser = bibtexparser.bparser.BibTexParser(common_strings=True)
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    # Convierte las entradas de la base de datos a un DataFrame de pandas
    df = pd.DataFrame(bib_database.entries)

    # Asegura que las columnas más importantes estén al principio para mejor visualización
    # Las columnas son: ID (el tag de cita) y ENTRYTYPE (article, book, etc.)
    columnas_principales = ['ID', 'ENTRYTYPE']
    columnas_existentes = [col for col in columnas_principales if col in df.columns]
    otras_columnas = [col for col in df.columns if col not in columnas_existentes]
    
    df = df[columnas_existentes + otras_columnas]

    # Escribe el DataFrame a un archivo de Excel
    # 'index=False' evita que se agregue una columna de índice innecesaria
    df.to_excel(ruta_excel, index=False, engine='openpyxl')

    print("✅ ¡Éxito!")
    print(f"Tus referencias han sido exportadas a:\n{ruta_excel}")

except FileNotFoundError:
    print(f"❌ ERROR: No se pudo encontrar el archivo en la ruta especificada.")
    print(f"Verifica que la ruta sea correcta: {ruta_bib}")
except Exception as e:
    print(f"❌ Ocurrió un error inesperado: {e}")