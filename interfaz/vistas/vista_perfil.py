import streamlit as st
from vistas.chat import render_chat
from config.configuraciones import cargar_arch_config, guardar_config, configurar_inicio_con_index
from utils.archivos.generar_vault import crear_vault

def mostrar():
    arch_config = cargar_arch_config()

    col1, col2 = st.columns([3, 2]) # vista perfil | chat
    with col1:
        with st.form(key="form_vault", clear_on_submit=True):

            col3, col4 = st.columns([9, 2]) # input path | botón

            with col3:
                st.session_state.path_vault = st.text_input("📁 Ingresá la ruta donde querés crear el Vault", key="input_path_form")
            with col4:
                submit = st.form_submit_button("➕ Agregar")

            if submit: # se supone que no hay creado nada en el path
                try:
                    arch_config["vault_path"] = st.session_state.path_vault
                    guardar_config(arch_config)

                    crear_vault(st.session_state.path_vault)

                    configurar_inicio_con_index(st.session_state.path_vault)

                    st.success(f"Vault creado en: {st.session_state.path_vault}")

                except Exception as e:
                    st.error("❌ Error al crear el Vault.")
                    st.exception(e)
    with col2:
        render_chat()
        if st.button("Volver"):
                st.session_state.vista = "inicio"
                st.rerun()