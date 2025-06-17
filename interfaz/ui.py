import streamlit as st
import sys
import os

# Agregar la ruta padre al path para importar main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import procesar_interaccion

#------------------------------------------------------------------------------

if "chat_whatsapp" not in st.session_state:
    st.session_state.chat_whatsapp = []


archivo = st.file_uploader("Subí un archivo")

if archivo:
    # Guardar archivo temporalmente
    ruta_archivo = f"temp/{archivo.name}"

st.title("Agente de estudio")

# mensaje = st.text_input("Escribí tu consulta")
 # Estilo para simular burbujas tipo WhatsApp
chat_style = """
<style>
.chat-container {
    height: 500px;
    overflow-y: auto;
    display: flex;
    flex-direction: column-reverse;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 10px;
    background-color: #f5f5f5;
}
.bubble {
    padding: 10px 15px;
    border-radius: 20px;
    margin: 5px;
    max-width: 70%;
    display: inline-block;
    word-wrap: break-word;
}
.user {
    background-color: #000000;
    align-self: flex-end;
    text-align: right;
}
.bot {
    background-color: #000000;
    align-self: flex-start;
    text-align: left;
}
</style>
"""

st.markdown(chat_style, unsafe_allow_html=True)

# Mostrar historial con burbujas
chat_html = '<div class="chat-container">'
for msg in reversed(st.session_state.chat_whatsapp):
    clase = "user" if msg["role"] == "Tú" else "bot"
    chat_html += f'<div class="bubble {clase}"><strong>{msg["role"]}</strong><br>{msg["text"]}</div>'
chat_html += '</div>'

st.markdown(chat_html, unsafe_allow_html=True)

with st.form("form_chat", clear_on_submit=True):
    user_input = st.text_input("Escribí tu mensaje", label_visibility="collapsed")
    submitted = st.form_submit_button("Enviar")
    mensaje = user_input

    if submitted and user_input:
        # resultado = procesar_interaccion(mensaje, ruta_archivo)
        resultado = procesar_interaccion(mensaje)
        
        st.session_state.chat_whatsapp.append({"role": "Tú", "text": user_input})
        st.session_state.chat_whatsapp.append({"role": "Agente", "text": f"Eco: {resultado}"})
        st.rerun()


# if st.button("Procesar"):
#     if mensaje and archivo:
#         # Guardar archivo temporalmente
#         ruta_archivo = f"temp/{archivo.name}"
#         with open(ruta_archivo, "wb") as f:
#             f.write(archivo.getbuffer())

#         resultado = procesar_interaccion(mensaje, ruta_archivo)

#         st.markdown("### Intención detectada:")
#         st.write(resultado["intencion"])

#         st.markdown("### Tema:")
#         st.write(resultado["tema"])

#         st.markdown("### Texto extraído:")
#         st.text_area("Texto", resultado["texto"][:1000])  # limitar vista
#     else:
#         st.warning("Cargá un mensaje y un archivo.")
