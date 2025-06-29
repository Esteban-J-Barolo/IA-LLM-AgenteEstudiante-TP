class ManejadorErrores:
    """
    Centraliza el manejo de errores y logging.
    """
    
    def __init__(self):
        self.errores_comunes = {
            "json_decode": "Error al procesar respuesta JSON",
            "rag_update": "Error al actualizar sistema RAG",
            "file_save": "Error al guardar archivo",
            "config_load": "Error al cargar configuración"
        }
    
    def manejar_error(self, tipo_error: str, excepcion: Exception, contexto: str = ""):
        """Maneja un error de forma centralizada."""
        mensaje = self.errores_comunes.get(tipo_error, "Error desconocido")
        print(f"❌ {mensaje}: {str(excepcion)}")
        if contexto:
            print(f"   Contexto: {contexto}")
        return {"error": mensaje, "detalle": str(excepcion)}
    
    def log_info(self, mensaje: str):
        """Registra información."""
        print(f"ℹ️  {mensaje}")
    
    def log_exito(self, mensaje: str):
        """Registra éxito."""
        print(f"✅ {mensaje}")