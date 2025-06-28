import streamlit as st
from vistas import vista_inicio, vista_perfil
from main import AgenteEstudio
from config.configuraciones import cargar_config_app

# cargar_config_app() # establece algunas configuraciones de variables globales

if "agente" not in st.session_state:
    with st.spinner("🤖 Cargando agente de estudio..."):
        try:
            st.session_state.agente = AgenteEstudio()
            st.session_state.materias = st.session_state.agente.get_materias()
            # nombres_materias = list(st.session_state.materias.keys())
            # st.session_state.agente.iniciar_rag(st.session_state.path_vault, nombres_materias)
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
