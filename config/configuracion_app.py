import json
from pathlib import Path
import shutil

class ConfiguracionApp:
    """
    Maneja la configuración de la aplicación.
    """
    
    def __init__(self):
        self.config_raw = self.cargar_arch_config()
        self.config = self._cargar_config()
    
    def _cargar_config(self):
        """Carga la configuración desde archivo."""
        return {
            'vault_path': self.config_raw["vault_path"],
            'materias': self.cargar_materias_desde_vault()
        }
    
    def cargar_arch_config(self, path="config/config.json") -> dict:
        path = Path(path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def cargar_materias_desde_vault(self):
    
        materias_path = Path(self.config_raw.get('vault_path')) / "Materias"

        if not materias_path.exists():
            return {}

        materias = {}

        for carpeta in materias_path.iterdir():
            if carpeta.is_dir():
                materias[carpeta.name] = {
                    "secciones": {
                        "TPs": [],
                        "Teoría": [],
                        "Práctica": [],
                        "Exámenes": []
                    }
                }

        return materias
    
    def guardar_config(self, datos: dict, path="config/config.json"):
        """Guarda la configuración."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    
    def get_vault_path(self):
        """Obtiene el path del vault."""
        return self.config.get('vault_path')
    
    def get_materias(self):
        """Obtiene las materias configuradas."""
        return self.config.get('materias', [])
    
    def actualizar_vault_path(self, nuevo_path):
        """Actualiza el path del vault."""
        self.config['vault_path'] = nuevo_path
        self.guardar_config(self.config)

    def establecer_config(self):
        self.ocultar_titulo()
        self.cargar_plugins(["templater-obsidian", "buttons"])

    def ocultar_titulo(self):
        app_path  = Path(self.get_vault_path()) / ".obsidian" / "app.json"
        app_path.parent.mkdir(parents=True, exist_ok=True)

        config = {}
        
        if app_path.exists():
            with open(app_path, "r", encoding="utf-8") as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError:
                    print("⚠️ El archivo app.json está dañado. Se sobreescribirá.")

        config["showInlineTitle"] = False

        with open(app_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    def cargar_plugins(self, plugins: list[str]):
        self.copiar_plugins()

        obsidian_path = Path(self.get_vault_path()) / ".obsidian"
        obsidian_path.mkdir(parents=True, exist_ok=True)

        # community-plugins.json → activa los plugins de terceros
        community_plugins_path = obsidian_path / "community-plugins.json"
        with open(community_plugins_path, "w", encoding="utf-8") as f:
            json.dump(plugins, f, indent=2)
        
        self.configurar_carpeta_templater("Plantillas/Crear")

    def configurar_carpeta_templater(self, carpeta_plantillas: str = "Plantillas"):
        templater_config = Path(self.get_vault_path()) / ".obsidian" / "plugins" / "templater-obsidian" / "data.json"
        
        # Crear carpeta si no existe
        templater_config.parent.mkdir(parents=True, exist_ok=True)
        
        # Si ya existe, cargar config actual, si no, usar base
        if templater_config.exists():
            with open(templater_config, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        # Establecer la carpeta de plantillas
        data["templates_folder"] = carpeta_plantillas
        data["user_scripts_folder"] = "Scripts"

        # Guardar configuración modificada
        with open(templater_config, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    
    def copiar_plugins(self):
        # Desde config/configuraciones.py
        ruta_actual = Path(__file__).parent  # config/
        ruta_base = ruta_actual.parent       # proyecto/
        origen_plugins = ruta_base / "Plugins"  # proyecto/Plugins/

        destino_plugins = Path(self.get_vault_path()) / ".obsidian" / "plugins"
        origen_plugins = Path(origen_plugins)

        destino_plugins.mkdir(parents=True, exist_ok=True)

        for plugin_folder in origen_plugins.iterdir():
            if plugin_folder.is_dir():
                destino_plugin = destino_plugins / plugin_folder.name
                if destino_plugin.exists():
                    shutil.rmtree(destino_plugin)
                shutil.copytree(plugin_folder, destino_plugin)

    def configurar_inicio_con_index(self):
        workspace_path = Path(self.get_vault_path()) / ".obsidian" / "workspace.json"
        
        if not workspace_path.exists():
            workspace_path.parent.mkdir(parents=True, exist_ok=True)
            data = {}
        else:
            with open(workspace_path, "r", encoding="utf-8") as f:
                data = json.load(f)

        # 🔧 1. Asegurar que "index.md" esté en el historial
        data["lastOpenFiles"] = ["index.md"] + [f for f in data.get("lastOpenFiles", []) if f != "index.md"]

        # 🔧 2. Reemplazar el contenido del panel principal con una pestaña de index.md
        data["main"] = {
            "id": "inicio",
            "type": "split",
            "children": [
                {
                    "id": "inicio-tab",
                    "type": "tabs",
                    "children": [
                        {
                            "id": "inicio-index",
                            "type": "leaf",
                            "state": {
                                "type": "markdown",
                                "state": {"file": "index.md"},
                                "icon": "lucide-file",
                                "title": "index"
                            }
                        }
                    ]
                }
            ],
            "direction": "vertical"
        }

        # 🔧 3. Establecer "index.md" como activo
        data["active"] = "inicio-index"

        # 💾 Guardar los cambios
        with open(workspace_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)