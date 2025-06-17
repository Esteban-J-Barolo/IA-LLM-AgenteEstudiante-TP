import streamlit as st
from vistas.chat import render_chat
import os
from pathlib import Path
import json
from utils.archivos.generar_archivos_principales import inicializar_archivos
from config.configuraciones import cargar_config, guardar_config

def mostrar():
    config = cargar_config()

    col1, col2 = st.columns([3, 2])
    with col1:
        with st.form(key="form_vault", clear_on_submit=True):

            col3, col4 = st.columns([9, 2])

            with col3:
                st.session_state.nuevo_vault = st.text_input("📁 Ingresá la ruta donde querés crear el Vault", key="input_path_form")
            with col4:
                submit = st.form_submit_button("➕ Agregar")

            if submit:
                # crear vault con direccion path
                try:
                    config["vault_path"] = st.session_state.nuevo_vault
                    guardar_config(config)

                    path_vault = crear_vault(st.session_state.nuevo_vault)
                    configurar_inicio_con_index(st.session_state.nuevo_vault)
                    st.session_state.vault_path = path_vault
                    st.success(f"Vault creado en: {path_vault}")
                except Exception as e:
                    st.error("❌ Error al crear el Vault.")
                    st.exception(e)
    with col2:
        render_chat()
        if st.button("Volver"):
                st.session_state.vista = "inicio"
                st.rerun()

def crear_vault(path_str: str):

    base = Path(path_str).expanduser().resolve()

    # Crear la estructura de carpetas
    carpetas = ["Materias", "Perfil", "Progreso", "Sistema"]
    for carpeta in carpetas:
        (base / carpeta).mkdir(parents=True, exist_ok=True)

    # Crear los archivos principales
    inicializar_archivos()

    return str(base)

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