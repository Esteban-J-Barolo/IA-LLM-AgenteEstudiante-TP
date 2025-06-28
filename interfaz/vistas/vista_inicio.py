import streamlit as st
from vistas.chat import render_chat

def mostrar():

    col1, col2 = st.columns([3, 1])
    with col1:
        render_chat()
    with col2:
        if st.button("## Perfil"):
            st.session_state.vista = "perfil"
            st.session_state.materia_seleccionada = None
            st.rerun()
            
        if st.button("### Chat"):
            st.session_state.materia_seleccionada = None
            st.session_state.chat = st.session_state.agente.cargar_chat_materia(st.session_state.materia_seleccionada)
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
                        st.session_state.agente.nueva_materia(nueva_materia)
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
                    st.session_state.chat = st.session_state.agente.cargar_chat_materia(nombre)
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
                        
                        archivo = st.file_uploader("📂", type=["txt", "md", "pdf", "docx"])
                        
                        if archivo:
                            if st.button("Guardar"):
                                with st.spinner("Guardando archivo y actualizando base de conocimientos..."):
                                    # Guardar archivo
                                    try:
                                        # Crear e iniciar el thread solo cuando se presiona el botón
                                        thread = st.session_state.agente.guardar_archivo_en_vault(
                                            archivo, 
                                            st.session_state.materia_seleccionada
                                        )
                                        thread.join()
                                        st.success("✅ Archivo guardado y base de conocimientos actualizándose en segundo plano!")
                                    except Exception as e:
                                        st.error(f"Error al guardar archivo: {e}")
        else:
            st.info("Todavía no cargaste materias.")

