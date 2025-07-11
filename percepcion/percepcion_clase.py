from config.configuracion_app import ConfiguracionApp
from servicios.gestor_archivos import GestorArchivos
from servicios.gestor_chat import GestorChat
from servicios.gestor_rag import GestorRAG
from servicios.validador_respuesta import ValidadorRespuesta
from razonamiento.razonamiento_clase import Razonamiento
from percepcion.clasificador_intencion import clasificar

class Percepcion:
    
    def __init__(self):
        self.configuracion = ConfiguracionApp()
        self.gestor_rag = GestorRAG(
            self.configuracion.get_vault_path(), 
            self.configuracion.get_materias()
        )
        self.gestor_archivos = GestorArchivos(self.configuracion.get_vault_path(), self.configuracion, self.gestor_rag)
        self.gestor_chat = GestorChat(self.configuracion.get_vault_path())
        self.validador = ValidadorRespuesta()
        self.razonamiento = Razonamiento()
    
    def procesar_interaccion(self, mensaje: str, materia: str):
        """Procesa una interacción del usuario."""
        try:
            # Clasificar intención
            intencion = clasificar(mensaje)
            
            # Buscar información
            if intencion.get('intencion') == 'resumen':
                informacion = self.gestor_rag.buscar_informacion(intencion.get("tema"))
            else:
                informacion = ''
            
            # Generar respuesta
            respuesta = self.razonamiento.generar_respuesta(intencion, informacion, materia)

            return respuesta
            
        except Exception as e:
            return {"error": f"Error en procesamiento: {str(e)}"}
    
    def nueva_materia(self, nombre: str):
        """Crea una nueva materia."""
        return self.gestor_archivos.crear_materia(nombre)
    
    def guardar_archivo_en_vault(self, archivo, materia: str):
        """Guarda un archivo en el vault."""
        return self.gestor_archivos.guardar_archivo(archivo, materia)
    
    def cargar_chat_materia(self, materia: str):
        """Carga el chat de una materia."""
        return self.gestor_chat.cargar_chat(materia)
    
    def guardar_chat_materia(self, chat: list, materia: str):
        """Guarda el chat de una materia."""
        return self.gestor_chat.guardar_chat(chat, materia)
    
    def actualizar_vault_path(self, nuevo_path: str):
        """Actualiza el path del vault."""
        self.configuracion.actualizar_vault_path(nuevo_path)
        # Actualizar componentes que dependen del path
        self.gestor_archivos = GestorArchivos(nuevo_path)
        self.gestor_rag = GestorRAG(nuevo_path, self.configuracion.get_materias())
        self.gestor_chat = GestorChat(nuevo_path)
    
    def traer_materias(self):
        return self.configuracion.get_materias()
    
    def guardar_nuevo_vault(self, nuevo_path: str):
        self.gestor_archivos.crear_vault(nuevo_path)
        self.configuracion.establecer_config()
