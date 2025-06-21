# Punto de entrada de la app (controlador general)
import json
import re
from typing import Dict, Optional
from llm_interface import Llm
import ast
from percepcion.clasificador_intencion import clasificar
from razonamiento.generar_salidas import respuesta

def procesar_interaccion(mensaje_usuario: str) -> dict:
# def procesar_interaccion(mensaje_usuario: str, ruta_archivo: str) -> dict:
    
    # procesador = ProcesadorArchivos()

    intencion = clasificar(mensaje_usuario)
    # texto = procesador.procesar_archivo(ruta_archivo)

    resumen = respuesta(intencion)

    respuesta_json = _extraer_json_de_respuesta(resumen)

    return resumen
    # return f"""
    #             "intencion": {intencion["intencion"]},
    #             "Respuesta": {respuesta_json.get("resumen")}
    #         """

def _extraer_json_de_respuesta(respuesta: str) -> Optional[Dict]:
        # """Extrae JSON de la respuesta del LLM, incluso si viene con texto adicional"""

        try:
            # Primero intentar parsear directamente
            return json.loads(respuesta.strip())
            # return ast.literal_eval(respuesta)
        except json.JSONDecodeError:
            # Si falla, buscar JSON dentro del texto
            json_pattern = r'\{[^{}]*\}'
            matches = re.findall(json_pattern, respuesta)
            
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
            # Si no se encuentra JSON válido, buscar patrones más complejos
            json_pattern_complex = r'\{.*\}'
            match = re.search(json_pattern_complex, respuesta, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
            return None