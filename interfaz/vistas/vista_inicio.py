import streamlit as st
from vistas.chat import render_chat
from utils.archivos.generar_materia import crear_archivos_materia
from config.configuraciones import cargar_config_app

def mostrar():
    cargar_config_app()

    col1, col2 = st.columns([3, 1])
    with col1:
        render_chat()
    with col2:
        if st.button("## Perfil"):
            st.session_state.vista = "perfil"
            st.rerun()
        
        st.markdown("### 📚 Materias")
        
        with st.form(key="form_materia", clear_on_submit=True):

            col1, col2 = st.columns(2)

            with col1:
                nueva_materia = st.text_input("Nombre de materia", key="input_materia_form")
            with col2:
                submit = st.form_submit_button("➕ Agregar")
            
            if submit:
                if nueva_materia:
                    if "materias" not in st.session_state:
                        st.session_state.materias = {}

                    if nueva_materia not in st.session_state.materias:
                        crear_archivos_materia(st.session_state.nuevo_vault, nueva_materia)
                        st.session_state.materias[nueva_materia] = {
                            "secciones": {"TPs": [], "Teoría": [], "Práctica": [], "Exámenes": []}
                        }
                        st.success(f"Materia '{nueva_materia}' agregada.")
                    else:
                        st.warning("Esa materia ya existe.")

                    st.rerun()
                else:
                    st.warning("Ingresá un nombre antes de agregar.")
            
        # Mostrar lista de materias existentes
        if "materias" in st.session_state and st.session_state.materias:
            st.markdown("#### Seleccioná una materia:")
            for nombre in st.session_state.materias:
                if st.button(f"📘 {nombre}"):
                    st.session_state.materia_seleccionada = nombre
                    st.rerun()
                col1, col2 = st.columns([2, 4])
                with col2:
                    if st.session_state.get("materia_seleccionada") == nombre:
                        st.markdown(f"##### Secciones de *{nombre}*")
                        if st.button("📖 Teoría", key=f"teoria_{nombre}"):
                            st.info("Sección Teoría abierta")
                        if st.button("🧪 Práctica", key=f"practica_{nombre}"):
                            st.info("Sección Práctica abierta")
                        if st.button("📂 TPs", key=f"tps_{nombre}"):
                            st.info("Sección TPs abierta")
                        if st.button("📝 Exámenes", key=f"examenes_{nombre}"):
                            st.info("Sección Exámenes abierta")
        else:
            st.info("Todavía no cargaste materias.")