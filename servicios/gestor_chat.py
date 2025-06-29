from utils.Chats.gestionar_chat import cargar_chat, guardar_chat

class GestorChat:
    """
    Maneja las operaciones de chat y conversaciones.
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
    
    def cargar_chat(self, materia: str):
        """Carga el historial de chat de una materia."""
        return cargar_chat(self.vault_path, materia)
    
    def guardar_chat(self, chat: list, materia: str):
        """Guarda el historial de chat."""
        return guardar_chat(chat, self.vault_path, materia)
    
    def limpiar_chat(self, materia: str):
        """Limpia el historial de chat."""
        pass
    
    def exportar_chat(self, materia: str, formato: str = "json"):
        """Exporta el chat en diferentes formatos."""
        pass