Organizar partituras puede ser una tarea tediosa y repetitiva, sobre todo cuando recibes decenas (o cientos) de archivos PDF mezclados, sin ningún criterio unificado: a veces son partituras separadas por instrumento, otras veces están todas en un único archivo, o incluso vienen en carpetas distintas.

Este script inteligente escanea automáticamente todas las partituras en formato PDF y detecta el instrumento al que pertenece cada página, usando técnicas avanzadas de OCR (reconocimiento óptico de caracteres) con EasyOCR, mejoras visuales con OpenCV, y un sistema de clasificación robusto basado en claves, patrones parciales y corrección de errores frecuentes.

Con solo ejecutarlo, el programa:

- Recorre automáticamente todas las subcarpetas dentro de partituras_originales/ en busca de archivos PDF.

- Extrae la cabecera de cada página del PDF y realiza OCR para leer el texto que suele indicar el instrumento.

- Interpreta el texto leído usando múltiples estrategias: coincidencias exactas, fragmentos de palabras, letras clave y hasta errores comunes de OCR como “sox alro” en lugar de “sax alto”.

- Clasifica cada página en su carpeta correspondiente dentro de partituras_ordenadas/, como sax_alto, clarinete, trompeta, etc.

- Las partituras que no puede clasificar con seguridad se guardan en una carpeta especial llamada No_Detectado, junto con una copia visual del encabezado leído para facilitar su revisión manual.

- Y además, incluye una herramienta para limpiar el contenido de trabajo en caso de que quieras empezar desde cero sin perder la estructura del proyecto.

¿Como se usa?

1. Instala las dependencias necesarias: pip install -r requirements.txt
2. Coloca tus partituras PDF en partituras_originales/. Pueden estar todas juntas o distribuidas en subcarpetas. El script lo detectará todo automáticamente.
3. Ejecuta el clasificador: python pdf_classifier.py  (O simplemente pulsa "run" en windows).

Este proyecto no es solo una herramienta útil, sino una forma de automatizar lo que antes llevaba horas de organización manual. Está pensado con cariño para bandas de música, profesores, archivistas, directores y músicos en general que quieren centrarse en la música y no en la burocracia de los archivos.
