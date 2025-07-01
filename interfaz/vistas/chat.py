import streamlit as st
from streamlit.components.v1 import html as components_html

def render_chat():

    if "chat" not in st.session_state:
        st.session_state.chat = st.session_state.agente.cargar_chat_materia(st.session_state.get("materia_seleccionada", "default"))

    # Debug: Mostrar cantidad de mensajes
    st.write(f"Mensajes en el chat: {len(st.session_state.chat)}")

    if st.session_state.chat:
        # Construir el HTML del chat
        chat_html = """
        <div class="chat-box" style="
            height: 400px;
            overflow-y: auto;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 12px;
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        ">
        """

        for i, msg in enumerate(st.session_state.chat):
            clase = "bubble-user" if msg["role"] == "Tú" else "bubble-agent"
            color = "#007bff" if clase == "bubble-user" else "#ffffff"
            text_color = "white" if clase == "bubble-user" else "#333"
            align = "right" if clase == "bubble-user" else "left"
            margin_align = "margin-left: 30%;" if clase == "bubble-user" else "margin-right: 30%;"
            border_color = "#007bff" if clase == "bubble-agent" else "transparent"
            
            # Procesar markdown y escapar caracteres especiales
            message_text = process_markdown_text(msg['text'])
            
            chat_html += f"""
            <div style="
                background-color: {color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 15px;
                padding: 12px 16px;
                margin: 8px 0;
                max-width: 70%;
                float: {align};
                clear: both;
                {margin_align}
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                word-wrap: break-word;
                white-space: pre-wrap;
                line-height: 1.4;
                font-size: 14px;
            ">
                <div style="
                    font-weight: bold;
                    margin-bottom: 6px;
                    font-size: 12px;
                    opacity: 0.8;
                ">{msg['role']} ({i+1})</div>
                <div>{message_text}</div>
            </div>
            """

        chat_html += """
        <div style="clear: both;"></div>
        </div>
        <script>
            // Scroll automático al final
            setTimeout(function() {
                const chatBox = document.querySelector('.chat-box');
                if (chatBox) {
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            }, 100);
            
            // Mejorar la visualización de emojis y caracteres especiales
            document.querySelectorAll('.chat-box div').forEach(function(div) {
                div.style.textRendering = 'optimizeLegibility';
            });
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
                    resultado = st.session_state.agente.procesar_interaccion(user_input.strip(), st.session_state.get("materia_seleccionada"))

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

                st.session_state.agente.guardar_chat_materia(st.session_state.chat, st.session_state.get("materia_seleccionada"))
                
                # Esperar un poco antes de rerun para que se vea la confirmación
                import time
                time.sleep(0.5)
                
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error al procesar el mensaje: {type(e).__name__}: {e}")
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

def process_markdown_text(text):
    """Procesa texto markdown para convertirlo a HTML"""
    import re

    # Escapar caracteres HTML básicos primero
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    # Procesar encabezados (### -> h3, ## -> h2, # -> h1)
    text = re.sub(r'^#### (.+)$', 
                    r'<h4 style="color: #2c3e50; margin: 12px 0 6px 0; font-size: 14px; font-weight: bold;">\1</h4>', 
                    text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', 
                    r'<h3 style="color: #2c3e50; margin: 15px 0 8px 0; font-size: 16px; font-weight: bold;">\1</h3>', 
                    text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', 
                    r'<h2 style="color: #2c3e50; margin: 18px 0 10px 0; font-size: 18px; font-weight: bold;">\1</h2>', 
                    text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', 
                    r'<h1 style="color: #2c3e50; margin: 20px 0 12px 0; font-size: 20px; font-weight: bold;">\1</h1>', 
                    text, flags=re.MULTILINE)
    
    # Procesar texto en negrita (**texto**)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong">\1</strong>', text)
    
    # Procesar texto en cursiva (*texto*)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    
    # Convertir saltos de línea
    text = text.replace('\n', '<br>')
    
    return text