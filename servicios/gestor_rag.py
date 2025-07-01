from utils.rag.iniciar_rag import iniciar_rag_con_actualizacion_incremental

class GestorRAG:
    """
    Maneja todas las operaciones relacionadas con el sistema RAG.
    """
    
    def __init__(self, vault_path: str, materias: list):
        self.vault_path = vault_path
        self.materias = materias
        self.rag = None
        self.inicializar()
    
    def inicializar(self):
        """Inicializa el sistema RAG."""
        self.rag = iniciar_rag_con_actualizacion_incremental(self.vault_path, self.materias)
    
    def actualizar(self, materias_incluir=None):
        """Actualiza el RAG con nuevos archivos."""
        self.rag = iniciar_rag_con_actualizacion_incremental(self.vault_path, materias_incluir)
    
    def buscar_informacion(self, tema: str):
        """Busca información relevante en el RAG."""
        return self.rag.search_and_format(tema)