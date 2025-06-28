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
    print("\n"+"-"*40+"\nPrompt para resumen\n"+prompt_clasificar, end="\n")
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
    “intencion": "una de las categorías listadas exactamente como aparece arriba",
    “contexto": "descripción breve (1-2 frases) del objetivo del mensaje"
    "tema": "Una frase que indique claramente el tema principal tratado"
    "preguntas": [
        "Pregunta 1 generada por el modelo",
        "Pregunta 2 generada por el modelo",
        "Pregunta 3 generada por el modelo"
    ]
}}

Reglas importantes:
No incluyas ningún texto adicional fuera del JSON.
Asegúrate de que la "intencion" debe coincidir exactamente con una de las categorías listadas arriba.
Usa \\n para representar saltos de línea dentro de strings si fuera necesario.
Escapa las comillas dobles (") dentro del contenido.

Instrucciones para generar las preguntas:
En la sección "preguntas", generá tres preguntas reflexivas que ayuden a:
Identificar el conocimiento o información necesaria para lograr el objetivo del mensaje.
Profundizar en lo que se debe incluir o tener en cuenta antes de resolver la tarea.
Planificar o elegir el mejor enfoque para desarrollar la tarea correctamente.
Las preguntas deben estar orientadas a que otro modelo (u otro paso) pueda responderlas y así prepararse mejor para ejecutar la tarea.
No deben referirse al formato, longitud o estilo del resultado final. Solo deben centrarse en el contenido necesario y la estrategia para abordarlo.
"""
    
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
                diccionario = respuesta_json
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