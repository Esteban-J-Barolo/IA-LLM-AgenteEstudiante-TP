from servicios.gestor_rag import GestorRAG
from servicios.validador_respuesta import ValidadorRespuesta
from servicios.gestor_archivos import GestorArchivos
from typing import List, Dict
from percepcion.clasificador_intencion import clasificar
from razonamiento.generar_salidas import respuesta
from generacion_contenido.generar_salidas_deseadas import generar_salida_deseada

class ProcesadorInteraccion:
    """
    Procesa las interacciones del usuario siguiendo el flujo completo.
    """
    
    def __init__(self, validador: ValidadorRespuesta, gestor_rag: GestorRAG, gestor_archivos: GestorArchivos):
        self.validador = validador
        self.gestor_rag = gestor_rag
        self.gestor_archivos = gestor_archivos
    
    def procesar(self, mensaje: str, materia: str, path_vault: str):
        """Procesa una interacción completa del usuario."""
        try:
            # Clasificar intención
            intencion = self._clasificar_intencion(mensaje)
            
            # Buscar información
            informacion = self.gestor_rag.buscar_informacion(intencion.get("tema"))
            
            # Generar respuesta
            respuesta_raw = self._generar_respuesta(intencion, informacion)
            
            # Validar respuesta
            resumen = self.validador.validar_y_procesar(respuesta_raw)
            
            if resumen:
                # Generar nota
                self._generar_nota(resumen.get("tema"), resumen.get("resumen"), resumen.get("conceptos"), materia)
                
                # Generar respuesta para usuario
                return self._generar_salida_usuario(resumen)
            
            return {"error": "No se pudo procesar la respuesta"}
            
        except Exception as e:
            return {"error": f"Error en procesamiento: {str(e)}"}
    
    def _clasificar_intencion(self, mensaje):
        """Clasifica la intención del mensaje."""
        return clasificar(mensaje)
    
    def _generar_respuesta(self, intencion, informacion):
        """Genera respuesta usando el LLM."""
        return respuesta(intencion, informacion)
    
    def _generar_nota(self, tema: str, resumen: str, conceptos: List[Dict[str, str]], materia: str):
        """Genera y guarda la nota de resumen."""
        self.gestor_archivos.generar_archivos_resumen(tema, resumen, conceptos, materia)
    
    def _generar_salida_usuario(self, resumen: str) -> str:
        """Genera la respuesta final para el usuario."""
        return generar_salida_deseada(resumen)