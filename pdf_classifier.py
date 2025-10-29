import os
import fitz  # PyMuPDF
import easyocr
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
import cv2
import numpy as np
from PIL import Image
import shutil

# CONFIGURACIÓN
INPUT_DIR = "partituras_originales"
OUTPUT_DIR = "partituras_ordenadas"
TEMP_IMG_DIR = "temp_images"
DESCONOCIDO_DIR = os.path.join(OUTPUT_DIR, "No_Detectado")
DEBUG_IMG_DIR = "debug_ocr"

# CREAR CARPETAS
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_IMG_DIR, exist_ok=True)
os.makedirs(DEBUG_IMG_DIR, exist_ok=True)
os.makedirs(DESCONOCIDO_DIR, exist_ok=True)

# LIMPIAR 'No_Detectado'
if os.path.exists(DESCONOCIDO_DIR):
    for archivo in os.listdir(DESCONOCIDO_DIR):
        ruta = os.path.join(DESCONOCIDO_DIR, archivo)
        if os.path.isfile(ruta):
            os.remove(ruta)
        elif os.path.isdir(ruta):
            shutil.rmtree(ruta)

# OCR CON EASYOCR
reader = easyocr.Reader(['es', 'en'])

# MEJORAR IMAGEN PARA OCR
def mejorar_imagen_para_ocr(imagen_pil):
    img = np.array(imagen_pil.convert("L"))
    img = cv2.bilateralFilter(img, 9, 75, 75)
    _, binarizada = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)
    return Image.fromarray(binarizada)

# CORREGIR TEXTO OCR
def normalizar_texto_ocr(texto):
    texto = texto.lower()
    reemplazos = {
        "aito": "alto", "a1to": "alto", "iz": "1º", "iº": "1º", "1°": "1º",
        "mi b": "mib", "mi♭": "mib", "saxo aito": "saxo alto", "sax0": "saxo",
        "flavta": "flauta", "clantnete": "clarinete", "clarinese": "clarinete",
        "tusmpas": "trompeta", "trampets": "trompeta", "bombkardina": "bombardino"
    }
    for error, correccion in reemplazos.items():
        texto = texto.replace(error, correccion)
    return texto

# INSTRUMENTOS (resumen)
INSTRUMENTOS = {
    # SAXOFÓN ALTO
    "saxofon alto": "sax_alto",
    "saxofón alto": "sax_alto",
    "alto sax": "sax_alto",
    "sax alto": "sax_alto",
    "alto saxophone": "sax_alto",
    "saxophone alto": "sax_alto",
    "sax: alto": "sax_alto",
    "saxo alto": "sax_alto",
    "saxo: alto": "sax_alto",
    "sax. alto": "sax_alto",
    "altosax": "sax_alto",
    "altosaxofon": "sax_alto",
    "altosaxophone": "sax_alto",
    "asax": "sax_alto",
    "alto": "sax_alto",
    "sox alro": "sax_alto",
     "sax alro": "sax_alto",

    # SAXOFÓN TENOR
    "saxofon tenor": "sax_tenor",
    "saxofón tenor": "sax_tenor",
    "tenor sax": "sax_tenor",
    "sax tenor": "sax_tenor",
    "tenor saxophone": "sax_tenor",
    "tenorsax": "sax_tenor",
    "tenorsaxofon": "sax_tenor",
    "tenorsaxophone": "sax_tenor",
    "tsax": "sax_tenor",

    # SAXOFÓN BARÍTONO
    "saxofon baritono": "sax_baritono",
    "saxofón barítono": "sax_baritono",
    "baritone sax": "sax_baritono",
    "sax baritono": "sax_baritono",
    "baritone saxophone": "sax_baritono",
    "barisax": "sax_baritono",
    "bsax": "sax_baritono",

    # TROMPETA
    "trompeta": "trompeta",
    "trumpet": "trompeta",
    "trp.": "trompeta",
    "tpt.": "trompeta",
    "tpt": "trompeta",
    "trp": "trompeta",
    "tp": "trompeta",
    "trumpet in b♭": "trompeta",
    "trumpet in bb": "trompeta",
    "trompeta en si♭": "trompeta",
    "trompeta en sib": "trompeta",
    "tr.": "trompeta",
    "trompfta": "trompeta",
    "trompkta": "trompeta",

    # CLARINETE
    "clarinete": "clarinete",
    "clarinet": "clarinete",
    "cl.": "clarinete",
    "cl": "clarinete",
    "clar.": "clarinete",
    "clarinet in b♭": "clarinete",
    "clarinet in bb": "clarinete",
    "clarinete en si♭": "clarinete",
    "clarinete en sib": "clarinete",
    "clarinetto": "clarinete",
    "clarinetto sib": "clarinete",
    "clarinetto in sib": "clarinete",

    # REQUINTO
    "requinto": "requinto",
    "requinto en mib": "requinto",
    "requinto en mi♭": "requinto",
    "eb clarinet": "requinto",
    "clarinete piccolo": "requinto",

    # FLAUTA
    "flauta": "flauta",
    "flute": "flauta",
    "flauta travesera": "flauta",
    "fl.": "flauta",
    "flute in c": "flauta",

    # FLAUTÍN
    "flautín": "flautin",
    "flautin": "flautin",
    "piccolo": "flautin",
    "piccolo flute": "flautin",

    # OBOE
    "oboe": "oboe",
    "hautbois": "oboe",

    # TROMPA
    "trompa": "trompa",
    "french horn": "trompa",
    "horn": "trompa",
    "corno": "trompa",
    "hn.": "trompa",

    # TROMBÓN
    "trombon": "trombon",
    "trombón": "trombon",
    "trombone": "trombon",
    "trb.": "trombon",
    "ironbön": "trombon",
    "trombön": "trombon",
    "ironbon": "trombon",

    # BOMBARDINO
    "bombardino": "bombardino",
    "euphonium": "bombardino",
    "baritone": "bombardino",
    "barítono": "bombardino",

    # TUBA
    "tuba": "tuba",
    "bass tuba": "tuba",
    "tuba en do": "tuba",
    "tuba en do♭": "tuba",
    "bb tuba": "tuba",
    "cc tuba": "tuba",
    "sousaphone": "tuba",

    # FLISCORNO
    "fliscorno": "fliscorno",
    "flugelhorn": "fliscorno",
    "flügelhorn": "fliscorno",
    "flgh.": "fliscorno",

    # BAJOS (genérico)
    "bajo": "bajo",
    "bajos": "bajo",
    "contrabajo": "bajo",
    "bass": "bajo",
    "string bass": "bajo",

    # CAJA
    "caja": "caja",
    "redoblante": "caja",
    "snare drum": "caja",
    "snare": "caja",
    "cajel": "caja",
    "ca j a": "caja",
    "caj a": "caja",

    # BOMBO
    "bombo": "bombo",
    "bass drum": "bombo",
    "gran cassa": "bombo",

    # PLATOS
    "platos": "platos",
    "cymbals": "platos",
    "piatti": "platos",

    # PERCUSIÓN GENERAL
    "percusión": "percusion",
    "percussion": "percusion",
    "multi-percussion": "percusion",
}

# DETECCIÓN DE INSTRUMENTO
def detectar_instrumento(texto):
    texto = normalizar_texto_ocr(texto)
    palabras = texto.split()

    # Búsqueda exacta
    for clave, carpeta in INSTRUMENTOS.items():
        if clave in texto:
            return carpeta

    # Heurísticas por prefijo, sufijo o subcadena
    for palabra in palabras:
        palabra = palabra.strip(",.():;-_").lower()

        # SAXOFÓN
        if palabra.startswith(("sax", "saxo", "saxof")) or "asax" in palabra or "bsax" in palabra or "tsax" in palabra:
            if "barit" in texto or "bsax" in palabra:
                return "sax_baritono"
            elif "tenor" in texto or "tsax" in palabra:
                return "sax_tenor"
            elif "alto" in texto or "asax" in palabra:
                return "sax_alto"
            else:
                return "sax_alto"

        # TROMPETA
        if palabra.startswith(("tr", "tru", "tromp")) or palabra.endswith(("eta", "mpeta")) or "rump" in palabra or "tpt" in palabra or "trp" in palabra:
            return "trompeta"

        # CLARINETE
        if palabra.startswith(("cla", "clar", "clari")) or palabra.endswith(("ete", "net", "inete")) or "clarine" in palabra or "cl." in palabra:
            return "clarinete"

        # FLAUTA
        if palabra.startswith(("fla", "flau")) or "flauta" in palabra:
            return "flauta"
        if "picc" in palabra or "flautín" in palabra or "picco" in palabra or "piccolo" in palabra:
            return "flautin"

        # REQUINTO
        if palabra.startswith("requ") or "requinto" in palabra or "eb clarinet" in texto:
            return "requinto"

        # OBOE
        if "obo" in palabra or "hautbois" in palabra:
            return "oboe"

        # TROMBÓN
        if palabra.startswith("trombo") or palabra.endswith(("bon", "bón", "bone")) or "trb" in palabra or "trbn" in palabra:
            return "trombon"

        # TROMPA
        if palabra.startswith(("horn", "corn", "tromp")) and "horn" in palabra or "corno" in palabra or "french horn" in texto or "hn." in palabra:
            return "trompa"

        # BOMBARDINO
        if palabra.startswith("bomb") or "euph" in palabra or "baritone" in palabra or "barítono" in palabra:
            return "bombardino"

        # TUBA
        if "tuba" in palabra or "sousa" in palabra:
            return "tuba"

        # FLISCORNO
        if palabra.startswith(("flis", "flug", "flüg")) or "fliscorno" in palabra or "flugelhorn" in palabra:
            return "fliscorno"

        # BAJO
        if "bajo" in palabra or "bass" in palabra or "contrabajo" in palabra:
            return "bajo"

        # CAJA
        if "caja" in palabra or "snare" in palabra or "redoblante" in palabra:
            return "caja"

        # BOMBO
        if "bombo" in palabra or "bass drum" in texto or palabra.startswith("bomb"):
            return "bombo"

        # PLATOS
        if "plato" in palabra or "piatti" in palabra or "cymbal" in palabra:
            return "platos"

        # PERCUSIÓN
        if "perc" in palabra or "percusión" in palabra or "percussion" in palabra:
            return "percusion"

    return None  # Si no se detecta nada


# PROCESAMIENTO DE PDF
def procesar_pdf(path_pdf):
    nombre_archivo = os.path.splitext(os.path.basename(path_pdf))[0]
    paginas = convert_from_path(path_pdf, dpi=200)

    for i, imagen in enumerate(paginas):
        imagen_path = os.path.join(TEMP_IMG_DIR, f"{nombre_archivo}_{i}.png")
        imagen.save(imagen_path)

        # Recorte ampliado para encabezado
        parte_superior = imagen.crop((0, 0, imagen.width, int(imagen.height * 0.4)))
        parte_superior = mejorar_imagen_para_ocr(parte_superior)

        # Guardar imagen debug
        debug_img_path = os.path.join(DEBUG_IMG_DIR, f"{nombre_archivo}_pag_{i+1}.png")
        parte_superior.save(debug_img_path)

        # OCR sobre parte superior
        resultado = reader.readtext(np.array(parte_superior))
        texto = "\n".join([linea[1] for linea in resultado])
        instrumento = detectar_instrumento(texto)

        # Fallback: OCR de toda la página si no se detecta instrumento
        if not instrumento:
            resultado_total = reader.readtext(np.array(imagen))
            texto_total = "\n".join([linea[1] for linea in resultado_total])
            texto_total = normalizar_texto_ocr(texto_total)
            instrumento = detectar_instrumento(texto_total)

            # Solo mostrar texto si sigue sin detectarse
            if not instrumento:
                print("-" * 40)
                print(f"[OCR NO DETECTADO] Página {i+1} de {nombre_archivo}:\n{texto_total}")
                print("-" * 40)

        # Crear carpeta destino según el instrumento
        carpeta_destino = os.path.join(OUTPUT_DIR, instrumento if instrumento else "No_Detectado")
        os.makedirs(carpeta_destino, exist_ok=True)

        # Guardar página como PDF
        lector = PdfReader(path_pdf)
        escritor = PdfWriter()
        escritor.add_page(lector.pages[i])
        salida_pdf = os.path.join(carpeta_destino, f"{nombre_archivo}_pag_{i+1}.pdf")
        with open(salida_pdf, "wb") as f_out:
            escritor.write(f_out)

        os.remove(imagen_path)


# EJECUCIÓN
for root, _, files in os.walk(INPUT_DIR):
    for archivo in files:
        if archivo.lower().endswith(".pdf"):
            path_pdf = os.path.join(root, archivo)
            procesar_pdf(path_pdf)


print("Clasificación finalizada con EasyOCR. Revisa 'partituras_ordenadas' y 'debug_ocr'.")