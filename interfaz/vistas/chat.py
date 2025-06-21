import streamlit as st
import sys
import os
from streamlit.components.v1 import html as components_html

# Agregar la ruta padre al path para importar main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import procesar_interaccion
from utils.Chats.gestionar_chat import cargar_chat, guardar_chat

def render_chat():

    if "chat" not in st.session_state:
        st.session_state.chat = cargar_chat(st.session_state.path_vault, st.session_state.get("materia_seleccionada"))

    # Debug: Mostrar cantidad de mensajes
    st.write(f"Mensajes en el chat: {len(st.session_state.chat)}")

    if st.session_state.chat:
        # Construir el HTML del chat
        chat_html = """
        <div class="chat-box" style="
            height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #f5f5f5;
        ">
        """

        for i, msg in enumerate(st.session_state.chat):
            clase = "bubble-user" if msg["role"] == "Tú" else "bubble-agent"
            color = "#007bff" if clase == "bubble-user" else "#e9ecef"
            text_color = "white" if clase == "bubble-user" else "#333"
            align = "right" if clase == "bubble-user" else "left"
            chat_html += f"""
            <div style="
                background-color: {color};
                color: {text_color};
                border-radius: 12px;
                padding: 8px 12px;
                margin: 6px 0;
                max-width: 70%;
                float: {align};
                clear: both;
            ">
                <strong>{msg['role']} ({i+1})</strong><br>{msg['text']}
            </div>
            """

        chat_html += """
        </div>
        <script>
            const chatBox = window.document.querySelector('.chat-box');
            if (chatBox) {
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        </script>
        """

        # Mostrar el componente con scroll activo
        components_html(chat_html, height=450, scrolling=True)
    else:
        st.info("¡Iniciá la conversación escribiendo un mensaje!")
    
    # Debug: Mostrar el state actual
    with st.expander("Debug - Ver estado del chat"):
        st.json(st.session_state.chat)
    
    # Formulario de chat
    st.markdown("### ✍️ Escribí tu mensaje")
    with st.form("form_chat", clear_on_submit=True):
        user_input = st.text_input(
            "Mensaje:", 
            placeholder="Preguntá algo sobre tu materia...",
            label_visibility="collapsed")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            submitted = st.form_submit_button("📤 Enviar")

        if submitted and user_input.strip():
            try:
                # Mostrar mensaje de procesamiento
                with st.spinner("🤖 El agente está pensando..."):
                    resultado = procesar_interaccion(user_input.strip())

                # Agregar mensajes al chat
                st.session_state.chat.append({
                    "role": "Tú", 
                    "text": user_input.strip()
                })
                st.session_state.chat.append({
                    "role": "Agente", 
                    "text": str(resultado)
                })

                # Mostrar confirmación
                st.success("✅ Mensaje enviado!")

                guardar_chat(st.session_state.chat, st.session_state.get("path_vault"), st.session_state.get("materia_seleccionada"))
                
                # Esperar un poco antes de rerun para que se vea la confirmación
                import time
                time.sleep(0.5)
                
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error al procesar el mensaje: {str(e)}")
                with st.expander("Ver detalles del error"):
                    st.exception(e)
        elif submitted and not user_input.strip():
            st.warning("⚠️ Por favor, escribí un mensaje antes de enviar")

    # Controles adicionales
    st.markdown("### 🛠️ Controles")
    col1, col2 = st.columns(2)
    
    if st.button("🗑️ Limpiar chat"):
        st.session_state.chat = []
        st.success("Chat limpiado!")
        st.rerun()

    if st.button("➕ Mensaje de prueba"):
        st.session_state.chat.append({
            "role": "Tú", 
            "text": "Mensaje de prueba del usuario"
        })
        st.session_state.chat.append({
            "role": "Agente", 
            "text": "Respuesta de prueba del agente"
        })
        st.success("Mensajes de prueba agregados!")
        st.rerun()