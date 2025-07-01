import streamlit as st
from interfaz.vistas.vista_inicio import mostrar_inicio
from interfaz.vistas.vista_perfil import mostrar_perfil
from percepcion.percepcion_clase import Percepcion

def iniciar():
    if "agente" not in st.session_state:
        with st.spinner("⏳ Cargando agente de estudio..."):
            try:
                st.session_state.agente = Percepcion()
                st.session_state.materias = st.session_state.agente.traer_materias()
            except Exception as e:
                st.error(f"Error al inicializar agente: {e}")
                st.session_state.agente = None
                st.stop()

    st.set_page_config(layout="wide")
    st.title("Agente de estudio")

    if "vista" not in st.session_state:
        st.session_state.vista = "inicio"

    if st.session_state.vista == "inicio":
        mostrar_inicio()
    elif st.session_state.vista == "perfil":
        mostrar_perfil()
