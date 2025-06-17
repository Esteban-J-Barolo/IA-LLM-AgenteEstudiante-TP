from llm_interface import Llm

class Respuestas():
    
    def __init__(self, intencion: dict):
        self.intencion = intencion
        pass

    def respuesta(self) -> dict:
    
        prompt = ''
        respuesta = ''

        if self.intencion.get("intencion") == 'resumen':
            # print(self.intencion)
            # print('-'*40)
            # print(self.intencion.get("contenido"))
            prompt = self._crear_prompt_resumen(self.intencion.get("contenido"))
            llm = Llm()
            respuesta = llm.enviar_mensaje(prompt)

        elif self.intencion.get("intencion") == 'agendar tarea':
            pass
        elif self.intencion.get("intencion") == 'hacer exámenes':
            pass
        elif self.intencion.get("intencion") == 'pregunta de una materia':
            pass
        elif self.intencion.get("intencion") == 'ninguno':
            pass
        else:
            pass

        return respuesta

    def _crear_prompt_resumen(self, contenido: str) -> str:

        # Detectar el tipo de contenido y longitud
        # longitud_contenido = len(contenido)

        # tipo_resumen = self._determinar_tipo_resumen(longitud_contenido, intencion)
        
        prompt = f"""Analiza el siguiente contenido y genera un resumen siguiendo estas instrucciones:

        CONTENIDO A RESUMIR:
        {contenido}

        FORMATO DE RESPUESTA:
        Responde ÚNICAMENTE con un JSON en este formato:
        {{
            "resumen": "tu resumen aquí",
            "puntos_clave": ["punto 1", "punto 2", "punto 3"],
            "longitud_resumen": "número de palabras del resumen",
            "temas_principales": ["tema 1", "tema 2"]
        }}

        REGLAS IMPORTANTES:
        - Mantén la información más relevante y elimina detalles secundarios
        - Usa un lenguaje claro y conciso
        - Preserva el tono y contexto del contenido original
        - No agregues información que no esté en el texto original
        - El resumen debe ser autocontenido y comprensible sin el texto original
        - Solo debes responder el JSON"""

        return prompt

    def _crear_prompt_agendar_tarea():
        pass

    def _crear_prompt_hacer_examen():
        pass

    def _crear_prompt_pregunta():
        pass