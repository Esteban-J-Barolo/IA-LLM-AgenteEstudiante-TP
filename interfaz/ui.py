import streamlit as st

from vistas import vista_inicio, vista_perfil
from main import AgenteEstudio

if "agente" not in st.session_state:
    try:
        st.session_state.agente = AgenteEstudio()
        # st.success("Agente inicializado correctamente")
    except Exception as e:
        st.error(f"Error al inicializar agente: {e}")
        st.session_state.agente = None

st.set_page_config(layout="wide")

st.title("Agente de estudio")

if "vista" not in st.session_state:
    st.session_state.vista = "inicio"

if st.session_state.vista == "inicio":
    vista_inicio.mostrar()
elif st.session_state.vista == "perfil":
    vista_perfil.mostrar()
