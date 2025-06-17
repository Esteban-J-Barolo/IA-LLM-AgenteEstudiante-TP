import streamlit as st

st.set_page_config(layout="wide")

# --- Estado inicial ---
if "materias" not in st.session_state:
    st.session_state.materias = {}
if "vista" not in st.session_state:
    st.session_state.vista = "inicio"
if "materia_seleccionada" not in st.session_state:
    st.session_state.materia_seleccionada = None
if "chat_general" not in st.session_state:
    st.session_state.chat_general = []
if "chat_whatsapp" not in st.session_state:
    st.session_state.chat_whatsapp = []

# ==============================
# VISTA INICIAL: Chat general a la derecha, botón de perfil a la izquierda
# ==============================
if st.session_state.vista == "inicio":
    col_izq, col_der = st.columns([0.8, 0.2])

    with col_der:
        st.title("🎓 Panel de Control")
        if st.button("Ir al Perfil Académico"):
            st.session_state.vista = "perfil"
            st.rerun()

        # Botón para agregar materia
        st.subheader("➕ Agregar materia")
        nueva_materia = st.text_input("Nombre de la materia")
        if st.button("Agregar materia"):
            if nueva_materia and nueva_materia not in st.session_state.materias:
                st.session_state.materias[nueva_materia] = {
                    "secciones": {"TPs": [], "Teoría": [], "Práctica": [], "Exámenes": []}
                }
                st.success(f"Materia '{nueva_materia}' agregada.")
            st.rerun()

        # Mostrar materias existentes
        st.subheader("📚 Materias")
        for nombre in st.session_state.materias:
            if st.button(f"Seleccionar: {nombre}"):
                st.session_state.materia_seleccionada = nombre
                st.session_state.vista = "materia"
                st.rerun()

    with col_izq:
        
        st.title("💬 Chat")

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

            if submitted and user_input:
                st.session_state.chat_whatsapp.append({"role": "Tú", "text": user_input})
                st.session_state.chat_whatsapp.append({"role": "Agente", "text": f"Eco: {user_input}"})
                st.rerun()

# ==============================
# VISTA PERFIL ACADÉMICO
# ==============================
elif st.session_state.vista == "perfil":
    st.title("👤 Perfil Académico")

    # Información general del perfil
    st.subheader("Información del perfil")
    st.write("Materias activas:", list(st.session_state.materias.keys()))
    st.write("Progreso estimado: 0%")
    st.write("Notas recientes: Ninguna")
    st.write("Tiempo dedicado: 0h")

    if st.button("⬅️ Volver al inicio"):
        st.session_state.vista = "inicio"
        st.session_state.materia_seleccionada = None
        st.rerun()

# ==============================
# VISTA MATERIA DETALLADA
# ==============================
elif st.session_state.vista == "materia":
    st.title(f"📘 {st.session_state.materia_seleccionada}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("TPs"):
            st.info("Sección de TPs seleccionada.")
    with col2:
        if st.button("Teoría"):
            st.info("Sección de Teoría seleccionada.")
    with col3:
        if st.button("Práctica"):
            st.info("Sección de Práctica seleccionada.")
    with col4:
        if st.button("Exámenes"):
            st.info("Sección de Exámenes seleccionada.")

    if st.button("⬅️ Volver al inicio"):
        st.session_state.vista = "inicio"
        st.session_state.materia_seleccionada = None
        st.rerun()
