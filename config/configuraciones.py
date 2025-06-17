import json
from pathlib import Path
import streamlit as st

def cargar_config(path="config/config.json") -> dict:
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
        
def cargar_config_app():
    config = cargar_config()
    st.session_state.nuevo_vault = config["vault_path"]
    st.session_state.materias = cargar_materias_desde_vault(st.session_state.nuevo_vault)
    ocultar_titulo()

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
    app_path  = Path(st.session_state.nuevo_vault) / ".obsidian" / "app.json"
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
