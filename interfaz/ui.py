import sys
from pathlib import Path

# Agregar el directorio padre al path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

import streamlit as st
from vistas import vista_inicio, vista_perfil
from main import AgenteEstudio

if "agente" not in st.session_state:
    with st.spinner("⏳ Cargando agente de estudio..."):
        try:
            st.session_state.agente = AgenteEstudio()
            st.session_state.materias = st.session_state.agente.traer_materias()
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
