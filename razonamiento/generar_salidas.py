from llm_interface import Llm
from typing import Dict

def respuesta(mensaje_procesado: Dict, informacion: str) -> Dict:

  if mensaje_procesado.get('intencion') == 'resumen':
    prompt = _crear_prompt_resumen(mensaje_procesado, informacion)
  else:
    prompt = _crear_prompt_ninguna(mensaje_procesado.get('contexto'), mensaje_procesado.get('tema'))

  llm = Llm()
  print("\n"+"-"*40+"\nPrompt\n"+prompt, end="\n")
  respuesta = llm.enviar_mensaje(prompt)
  print("\nRespuesta\n"+respuesta+"\n"+"-"*40, end="\n")

  return respuesta

def _crear_prompt_resumen(mensaje_procesado: Dict, informacion: str) -> str:
    
    prompt = f"""{mensaje_procesado.get("contexto")}

Preguntas relevantes a considerar:
{mensaje_procesado.get("preguntas")}

Hace el resumen en base a esta información:
{informacion}

Responde ÚNICAMENTE con un JSON en el siguiente formato:
{{
"resumen": “Un resumen muy breve, redactado con lenguaje claro. Los conceptos en este resumen que son clave y más complejos deben estar etre dobles corchetes como [[NombreConcepto]]."
"tema": "Una frase que indique claramente el tema principal tratado en el resumen."
"conceptos": [
    {{
      "concepto": "Nombre del concepto clave o difícil mencionado en el resumen",
      "desarrollo": "Explicación clara y concisa del concepto, pensada para entenderse dentro de una nota de Obsidian."
    }},
    {{
      "concepto": "...",
      "desarrollo": "..."
    }}
    // ...más conceptos si es necesario
  ]
"ejemplos": “una situación concreta, analogía o aplicación práctica que ayude a entender ese concepto”
"referencias": [
    {{  
      "referencia": "Nombre del archivo de donde se saco la información"
    }},
    {{
      "referencia": "..."
    }},
    // ...más referencias si es necesario
}}

Instrucciones adicionales:
No incluyas ningún texto adicional fuera del JSON.
Usa \\n para representar saltos de línea dentro de strings si fuera necesario.
Escapa las comillas dobles (") dentro del contenido.
Asegurate de que cada concepto mencionado en el resumen esté también incluido en el array "conceptos", con su explicación correspondiente.
El resumen debe ser breve, directo y no repetir los desarrollos ya presentes en el campo "conceptos".
Restricciones de TEMA:
   - NO debe contener : / \ | < > " ' * ?
   - Reemplaza : por -
   - Mantén solo letras, números, espacios, guiones y paréntesis
   - Máximo 80 caracteres
"""

    return prompt

def _crear_prompt_agendar_tarea():
    pass

def _crear_prompt_hacer_examen():
    pass

def _crear_prompt_pregunta():
    pass

def _crear_prompt_ninguna(msj: str, tema: str):
    return f"""Actuás como un agente inteligente que ayuda y motiva a estudiantes universitarios a aprender mejor. Tu especialidad es generar resúmenes de textos académicos y ayudar a comprender los temas clave.

Vas a recibir un mensaje del estudiante que fue clasificado como "ninguna" (es decir, no es un resumen).

Tu tarea es generar una respuesta clara, empática y útil para el estudiante. La respuesta debe cumplir los siguientes objetivos:

1. Explicar brevemente por qué su mensaje no fue reconocido como un resumen.
2. Invitar al estudiante a reformular o compartir un texto académico que quiera resumir.
3. Motivar con una frase alentadora para que siga aprendiendo y aprovechando el asistente.

Usá un tono cercano, positivo y motivador, como si fueras un tutor que quiere ayudar a mejorar el hábito de estudio.

Formato de salida: texto plano en español (no JSON).

Información disponible:
- mensaje_original: {msj}
- tema: {tema}

⚠️ Importante:
- No incluyas títulos, encabezados, etiquetas, ni aclaraciones como "Respuesta motivadora", "Mensaje generado por IA", etc.
- Empezá directamente con el mensaje que el agente le diría al estudiante.
"""