# Lee archivos markdown o texto plano

import os

class ProcesadorArchivos:
    def __init__(self):
        pass

    def procesar_archivo(self, ruta: str) -> str:
        if not os.path.exists(ruta):
            return f"[ERROR] El archivo no existe: {ruta}"

        if ruta.endswith(".md") or ruta.endswith(".txt"):
            with open(ruta, "r", encoding="utf-8") as f:
                return f.read()

        elif ruta.endswith(".pdf"):
            try:
                import PyPDF2
                texto = ""
                with open(ruta, "rb") as f:
                    lector = PyPDF2.PdfReader(f)
                    for pagina in lector.pages:
                        texto += pagina.extract_text()
                return texto
            except Exception as e:
                return f"[ERROR] No se pudo leer PDF: {e}"

        else:
            return "[ERROR] Tipo de archivo no soportado"
