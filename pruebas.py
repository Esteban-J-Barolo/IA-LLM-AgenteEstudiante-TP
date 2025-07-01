from llm_interface import Llm

llm = Llm()

msj_resumen = """
Preguntas relevantes a considerar:
¿Qué conocimiento previo de física y química sería útil tener en cuenta antes de abordar esta tarea?", "¿Qué información clave sobre las leyes de la termodinámica, la energía y la entropía debe incluirse para cumplir con el objetivo del mensaje?", "¿Qué enfoque o estrategia sería más adecuada para presentar la información de manera clara y concisa, como utilizar ejemplos prácticos o diagramas para ilustrar los conceptos?"

Hace el resumen en base a esta información:
Tu base de conocimiento

Responde ÚNICAMENTE con un JSON en el siguiente formato:
{{
“resumen": “Un resumen muy breve, redactado con lenguaje claro. Los conceptos en este resumen que son clave y más complejos deben estar etre dobles corchetes como [[NombreConcepto]]."
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
# ¿Cuáles son las diferencias entre UDP y TCP?
# El principio de encapsulamiento en la programación orientada a objetos permite ocultar la implementación interna de una clase, exponiendo solo lo necesario a través de interfaces públicas. Esto mejora la modularidad, la seguridad y facilita el mantenimiento del código.

msj_clasificacion ="""
Experto: Analista de intención y propósito académico 
Tu rol es analizar mensajes de estudiantes para identificar si contienen un resumen o no, y brindar contexto y metainformación útil para otros modelos o etapas de procesamiento.

Analiza el siguiente mensaje y clasifícalo en una de estas categorías:
resumen, ninguna

Mensaje a clasificar:

¿Cuáles son las diferencias entre UDP y TCP?

Responde ÚNICAMENTE con un JSON en el siguiente formato:
{{
“intencion": "una de las categorías listadas exactamente como aparece arriba",
“contexto": "descripción breve (1-2 frases) del objetivo del mensaje",
"tema": "Si 'intencion' es 'resumen', debe indicar el tema principal tratado. Si es 'ninguna', debe explicar por qué el mensaje no corresponde a un resumen.",
"consideraciones": [
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
En la sección "consideraciones", generá tres preguntas reflexivas que ayuden a:
- Identificar el conocimiento o información necesaria para lograr el objetivo del mensaje.
- Profundizar en lo que se debe incluir o tener en cuenta antes de resolver la tarea.
- Planificar o elegir el mejor enfoque para desarrollar la tarea correctamente.

Las preguntas deben estar orientadas a que otro modelo (u otro paso) pueda responderlas y así prepararse mejor para ejecutar la tarea.  
No deben referirse al formato, longitud o estilo del resultado final. Solo deben centrarse en el contenido necesario y la estrategia para abordarlo.
"""

msj_ninguna = """
Actuás como un agente inteligente que ayuda y motiva a estudiantes universitarios a aprender mejor. Tu especialidad es generar resúmenes de textos académicos y ayudar a comprender los temas clave.

Vas a recibir un mensaje del estudiante que fue clasificado como "ninguna" (es decir, no es un resumen).

Tu tarea es generar una respuesta clara, empática y útil para el estudiante. La respuesta debe cumplir los siguientes objetivos:

1. Explicar brevemente por qué su mensaje no fue reconocido como un resumen.
2. Invitar al estudiante a reformular o compartir un texto académico que quiera resumir.
3. Motivar con una frase alentadora para que siga aprendiendo y aprovechando el asistente.

Usá un tono cercano, positivo y motivador, como si fueras un tutor que quiere ayudar a mejorar el hábito de estudio.

Formato de salida: texto plano en español (no JSON).

Información disponible:
- mensaje_original: ¿Cuáles son las diferencias entre UDP y TCP?
- tema: "No aplica, ya que la intención no es un resumen. La pregunta se centra en las diferencias entre UDP y TCP."

⚠️ Importante:
- No incluyas títulos, encabezados, etiquetas, ni aclaraciones como "Respuesta motivadora", "Mensaje generado por IA", etc.
- Empezá directamente con el mensaje que el agente le diría al estudiante.
"""

def llm_1(msj):
    return llm.enviar_mensaje(msj)

print(llm_1(msj_ninguna))