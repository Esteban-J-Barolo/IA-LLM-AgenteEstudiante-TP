import streamlit as st

from vistas import vista_inicio, vista_perfil, vista_materia
st.set_page_config(layout="wide")

st.title("Agente de estudio")

if "vista" not in st.session_state:
    st.session_state.vista = "inicio"

if st.session_state.vista == "inicio":
    vista_inicio.mostrar()
elif st.session_state.vista == "perfil":
    vista_perfil.mostrar()
elif st.session_state.vista == "materia":
    vista_materia.mostrar()
