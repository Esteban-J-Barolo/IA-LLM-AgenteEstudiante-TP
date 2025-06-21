# Clasifica el tipo de intención a partir de un mensaje
import json
import re
from typing import Dict, Optional
from llm_interface import Llm

def clasificar(mensaje: str) -> Dict:
    mensaje_lower = mensaje.lower()
    clasificaciones_posibles = [
                                'resumen', 
                                'agendar tarea', 
                                'hacer exámenes', 
                                'pregunta de una materia', 
                                'ninguno'
                                ]

    # Crear el prompt estructurado
    prompt_clasificar = _crear_prompt_clasificacion(mensaje_lower, clasificaciones_posibles)

    # Aquí llamarías a tu API de LLM
    respuesta_clasificar = _llamar_llm(prompt_clasificar)

    # Procesar la respuesta y crear el diccionario
    diccionario = _procesar_respuesta(respuesta_clasificar, mensaje_lower, clasificaciones_posibles)

    # print(diccionario)

    return diccionario

def _crear_prompt_clasificacion(mensaje: str, clasificaciones_posibles: list) -> str:
    # """Crea un prompt estructurado para la clasificación"""

    clasificaciones_str = ", ".join([f"'{c}'" for c in clasificaciones_posibles])
    
    prompt = f"""Analiza el siguiente mensaje y clasifícalo en una de estas categorías:
                {clasificaciones_str}

                Mensaje a clasificar: "{mensaje}"

                Responde ÚNICAMENTE con un JSON en el siguiente formato:
                {{
                    "intencion": "categoria_elegida",
                    "tema": "tema académico principal mencionado, si lo hay"
                    "confianza": número entre 0 y 1 que represente cuán seguro estás (por ejemplo: 0.95),
                    "razonamiento": "breve explicación de por qué clasificaste el mensaje de esa forma",
                    "contenido": "Generar un contenido de 200 palabras si la intención es resumir, en otro caso dejar sin nada"
                }}

                Asegúrate de que la "intencion" sea exactamente una de las categorías listadas arriba.
                En el campo "contenido", usa \\n en vez de saltos de línea y escapá todas las comillas dobles. O bien, devolvé el contenido como una lista de strings línea por línea."""
    
    return prompt

def _llamar_llm(prompt: str) -> str:
    # """
    # Placeholder para la llamada a tu API de LLM
    # Reemplaza esto con tu implementación real
    # """
    llm = Llm()
    respuesta = llm.enviar_mensaje(prompt)
    # print(respuesta)
    return respuesta

def _procesar_respuesta(respuesta_llm: str, mensaje_original: str, clasificaciones_posibles: list) -> Dict:
    # """Procesa la respuesta del LLM y crea el diccionario final"""

    try:
        # Intentar parsear la respuesta como JSON
        respuesta_json = _extraer_json_de_respuesta(respuesta_llm)

        # print(respuesta_json)
        
        if respuesta_json and "intencion" in respuesta_json:
            intencion = respuesta_json["intencion"].lower()
            
            # Validar que la intención esté en las clasificaciones posibles
            if intencion in clasificaciones_posibles:
                diccionario = {
                    "intencion": intencion,
                    "tema": respuesta_json.get("tema", ""),
                    "confianza": respuesta_json.get("confianza", 0.0),
                    "razonamiento": respuesta_json.get("razonamiento", ""),
                    "contenido": respuesta_json.get("contenido", "")
                }
            else:
                # Si la intención no es válida, usar 'ninguno'
                diccionario = {
                    "intencion": "ninguno",
                    "tema": respuesta_json.get("tema", ""),
                    "confianza": 0.0,
                    "razonamiento": f"Intención no reconocida: {intencion}",
                    "contenido": "contenido"
                }
        else:
            # Si no se puede parsear, usar 'ninguno'
            diccionario = {
                "intencion": "ninguno",
                "tema": respuesta_json.get("tema", ""),
                "confianza": 0.0,
                "razonamiento": "Error al procesar respuesta del LLM",
                "contenido": "contenido"
            }
            
    except Exception as e:
        tema_fallback = ""
        try:
            tema_fallback = respuesta_json.get("tema", "") if respuesta_json else ""
        except:
            tema_fallback = ""

        diccionario = {
            "intencion": "ninguno",
            "tema": tema_fallback,
            "confianza": 0.0,
            "razonamiento": f"Error en procesamiento: {str(e)}",
            "contenido": "contenido"
        }
            
    return diccionario

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