import json
from pathlib import Path
import streamlit as st
import shutil
        
def cargar_config_app():
    config = cargar_arch_config()
    st.session_state.path_vault = config["vault_path"]
    st.session_state.materias = cargar_materias_desde_vault(st.session_state.path_vault)

def establecer_config():
    ocultar_titulo()
    cargar_plugins(["templater-obsidian", "buttons"])
    configurar_inicio_con_index(st.session_state.path_vault)

def cargar_arch_config(path="config/config.json") -> dict:
    path = Path(path)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_config(datos: dict, path="config/config.json"):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def cargar_materias_desde_vault(vault_path: str):
    
    materias_path = Path(vault_path) / "Materias"

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

def ocultar_titulo():
    app_path  = Path(st.session_state.path_vault) / ".obsidian" / "app.json"
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

def cargar_plugins(plugins: list[str]):
    copiar_plugins("C:/Users/Esteban/Desktop/UTN/UTN 2025/IA/TP 2 IA/Agente_estudio/Plugins")

    obsidian_path = Path(st.session_state.path_vault) / ".obsidian"
    obsidian_path.mkdir(parents=True, exist_ok=True)

    # community-plugins.json → activa los plugins de terceros
    community_plugins_path = obsidian_path / "community-plugins.json"
    with open(community_plugins_path, "w", encoding="utf-8") as f:
        json.dump(plugins, f, indent=2)
    
    configurar_carpeta_templater("Plantillas/Crear")

def configurar_carpeta_templater(carpeta_plantillas: str = "Plantillas"):
    templater_config = Path(st.session_state.path_vault) / ".obsidian" / "plugins" / "templater-obsidian" / "data.json"
    
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

def copiar_plugins(origen_plugins: str):
    destino_plugins = Path(st.session_state.path_vault) / ".obsidian" / "plugins"
    origen_plugins = Path(origen_plugins)

    destino_plugins.mkdir(parents=True, exist_ok=True)

    for plugin_folder in origen_plugins.iterdir():
        if plugin_folder.is_dir():
            destino_plugin = destino_plugins / plugin_folder.name
            if destino_plugin.exists():
                shutil.rmtree(destino_plugin)
            shutil.copytree(plugin_folder, destino_plugin)

def configurar_inicio_con_index(vault_path: str):
    workspace_path = Path(vault_path) / ".obsidian" / "workspace.json"
    
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