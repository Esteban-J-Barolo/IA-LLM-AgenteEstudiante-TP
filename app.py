import streamlit as st
from interfaz.ui import iniciar

# Configuración de la página
st.set_page_config(
    page_title="Agente Estudio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("Agente Estudio")

if __name__ == "__main__":
    iniciar()