from llm_interface import Llm
from typing import Dict

def respuesta(mensaje_procesado: Dict, informacion: str) -> Dict:

    prompt = _crear_prompt_resumen(mensaje_procesado, informacion)
    print("\n"+"-"*40+"\nPrompt para resumen\n"+prompt, end="\n")
    llm = Llm()
    respuesta = llm.enviar_mensaje(prompt)
    print("-"*40, "\nRespeusta agente\n", respuesta)

    # if intencion.get("intencion") == 'resumen':
    #     prompt = _crear_prompt_resumen(intencion.get("contenido"))
    #     llm = Llm()
    #     respuesta = llm.enviar_mensaje(prompt)

    # elif intencion.get("intencion") == 'agendar tarea':
    #     pass
    # elif intencion.get("intencion") == 'hacer exámenes':
    #     pass
    # elif intencion.get("intencion") == 'pregunta de una materia':
    #     pass
    # elif intencion.get("intencion") == 'ninguno':
    #     pass
    # else:
    #     pass

    return respuesta

def _crear_prompt_resumen(mensaje_procesado: Dict, informacion: str) -> str:

    # Detectar el tipo de contenido y longitud
    # longitud_contenido = len(contenido)

    # tipo_resumen = self._determinar_tipo_resumen(longitud_contenido, intencion)
    
    prompt = f"""{mensaje_procesado.get("contexto")}

Preguntas relevantes a considerar:
{mensaje_procesado.get("preguntas")}

Hace el resumen en base a esta información:
{informacion}

Responde ÚNICAMENTE con un JSON en el siguiente formato:
{{
“resumen": “Un resumen **muy breve**, redactado con lenguaje claro. Los conceptos clave y más complejos deben estar conectados a notas de Obsidian (por ejemplo, usando enlaces como [[NombreConcepto]])."
“tema": "Una frase que indique claramente el tema principal tratado en el resumen."
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
“ejemplos”: “una situación concreta, analogía o aplicación práctica que ayude a entender ese concepto”
}}

Instrucciones adicionales:
No incluyas ningún texto adicional fuera del JSON.
Usa \\n para representar saltos de línea dentro de strings si fuera necesario.
Escapa las comillas dobles (") dentro del contenido.
Asegurate de que cada concepto mencionado en el resumen esté también incluido en el array "conceptos", con su explicación correspondiente.
El resumen debe ser breve, directo y no repetir los desarrollos ya presentes en el campo "conceptos".
"""

    return prompt

def _crear_prompt_agendar_tarea():
    pass

def _crear_prompt_hacer_examen():
    pass

def _crear_prompt_pregunta():
    pass