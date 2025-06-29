from config.configuraciones import cargar_config_app

class ConfiguracionApp:
    """
    Maneja la configuración de la aplicación.
    """
    
    def __init__(self):
        self.config = self._cargar_config()
    
    def _cargar_config(self):
        """Carga la configuración desde archivo."""
        return cargar_config_app()
    
    def guardar_config(self, nueva_config):
        """Guarda la configuración."""
        pass
    
    def get_vault_path(self):
        """Obtiene el path del vault."""
        return self.config.get('path_vault')
    
    def get_materias(self):
        """Obtiene las materias configuradas."""
        return self.config.get('materias', [])
    
    def actualizar_vault_path(self, nuevo_path):
        """Actualiza el path del vault."""
        self.config['path_vault'] = nuevo_path
        self.guardar_config(self.config)