from generacion_contenido.generacion_contenido_clase import GenerarContenido
from servicios.validador_respuesta import ValidadorRespuesta
from memoria.memoria_clase import Memoria
from razonamiento.generar_salidas import respuesta
import json

class Razonamiento:

    def __init__(self):
        self.generar_contenido = GenerarContenido()
        self.memoria = Memoria()
        self.validador = ValidadorRespuesta()
        
    def generar_respuesta(self, intencion, informacion, materia: str):
        """Genera respuesta usando el LLM."""

        respuesta_raw = respuesta(intencion, informacion)

        if intencion.get('intencion') == 'resumen':

            # Validar respuesta
            resumen = self.validador.validar_y_procesar(respuesta_raw)

            # Generar nota
            self.memoria.generar_las_nota(resumen, materia)
            
            # Generar respuesta para usuario
            return self.generar_contenido.dar_respuesta_resumen(resumen)
        else:
            return respuesta_raw