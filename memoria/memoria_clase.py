
from typing import List, Dict
from servicios.gestor_archivos import GestorArchivos
from config.configuracion_app import ConfiguracionApp
from servicios.gestor_rag import GestorRAG

class Memoria:

    def __init__(self):
        self.configuracion = ConfiguracionApp()
        self.gestor_rag = GestorRAG(
            self.configuracion.get_vault_path(), 
            self.configuracion.get_materias()
        )
        self.gestor_archivos = GestorArchivos(self.configuracion.get_vault_path(), self.configuracion, self.gestor_rag)

    # def generar_las_nota(self, tema: str, resumen: str, conceptos: List[Dict[str, str]], materia: str):
    def generar_las_nota(self, infromacion: Dict, materia: str):
        self.gestor_archivos.generar_archivos_resumen(infromacion, materia)