from typing import List, Dict
import threading
from servicios.gestor_rag import GestorRAG
from servicios.configuracion_app import ConfiguracionApp
from utils.archivos.generar_nota_resumen import generar_nota_resumen
from config.configuraciones import guardar_config, configurar_inicio_con_index
from utils.archivos.generar_vault import crear_vault
from utils.archivos.generar_materia import crear_archivos_materia
from utils.archivos.procesador_archivos import guardar_en_vault

class GestorArchivos:
    """
    Maneja todas las operaciones relacionadas con archivos y el vault.
    """
    
    def __init__(self, vault_path: str, configuracion: ConfiguracionApp, gestor_rag: GestorRAG):
        self.vault_path = vault_path
        self.configuracion = configuracion
        self.gestor_rag = gestor_rag
    
    def crear_materia(self, nombre: str):
        """Crea una nueva materia en el vault."""
        crear_archivos_materia(self.vault_path, nombre)
    
    def guardar_archivo(self, archivo, materia: str):
        """Guarda un archivo en el vault."""
        guardar_en_vault(archivo, self.vault_path, materia)

        thread = threading.Thread(
            target=self.gestor_rag.actualizar,
            args=(self.configuracion.get_materias(),)
        )
        thread.daemon = True
        thread.start()

        return thread

    def crear_vault(self, path: str):
        """Crea un nuevo vault."""
        self.vault_path = path

        self.configuracion.actualizar_vault_path(path)

        crear_vault(path)

        configurar_inicio_con_index(path)
    
    def validar_estructura_vault(self):
        """Valida que el vault tenga la estructura correcta."""
        pass

    def generar_archivos_resumen(self, tema: str, informacion: str, conceptos: List[Dict[str, str]], materia: str):
        generar_nota_resumen(self.vault_path, tema, informacion, conceptos, materia)
