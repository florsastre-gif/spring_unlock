import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SPRING UNLOCK 🧭", layout="centered")

with st.sidebar:
    st.title("Configuración")
    user_api_key = st.text_input("Ingresá tu Google API Key", type="password")

if not user_api_key:
    st.title("🧭 SPRING UNLOCK")
    st.stop()

genai.configure(api_key=user_api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🧭 SPRING UNLOCK")

with st.form("spring_form"):
    nombre = st.text_input("Nombre", placeholder="Laura")
    negocio = st.text_input("Negocio", placeholder="Centro de Pilates")
    enfoque = st.text_input("¿Qué activamos hoy?", placeholder="Promo 2x1")
    
    col1, col2, col3 = st.columns(3)
    with col1: precio = st.text_input("Precio", placeholder="$15.000")
    with col2: limite = st.text_input("Límite", placeholder="Viernes")
    with col3: canal = st.selectbox("Canal", ["WhatsApp", "Instagram"])
    
    detalles = st.text_area("Contexto (caos/idea):")
    submit = st.form_submit_button("Calibrar Brújula 🚀")

if submit:
    if not nombre or not detalles:
        st.warning("Faltan datos.")
    else:
        with st.spinner("Decidiendo..."):
            import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SPRING UNLOCK 🧭", layout="centered")

with st.sidebar:
    st.title("Configuración")
    user_api_key = st.text_input("Ingresá tu Google API Key", type="password")
    st.info("Obtené tu llave en [Google AI Studio](https://aistudio.google.com/app/apikey)")

if not user_api_key:
    st.title("🧭 SPRING UNLOCK")
    st.stop()

genai.configure(api_key=user_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🧭 SPRING UNLOCK")

with st.form("spring_form"):
    nombre = st.text_input("Nombre", placeholder="Laura")
    negocio = st.text_input("Negocio", placeholder="Centro de Pilates")
    enfoque = st.text_input("¿Qué activamos hoy?", placeholder="Promo 2x1")
    
    col1, col2, col3 = st.columns(3)
    with col1: precio = st.text_input("Precio", placeholder="$15.000")
    with col2: limite = st.text_input("Límite", placeholder="Viernes")
    with col3: canal = st.selectbox("Canal", ["WhatsApp", "Instagram"])
    
    detalles = st.text_area("Contexto (caos/idea):")
    submit = st.form_submit_button("Calibrar Brújula 🚀")

if submit:
    if not nombre or not detalles:
        st.warning("Faltan datos.")
    else:
        with st.spinner("Decidiendo..."):
            # PROMPT RESTRUCTURADO: Eliminamos validación, criterio y relleno.
            prompt = f"""
            Actuá como estratega senior de ejecución. 
            Usuaria: {nombre}. Negocio: {negocio}.
            Objetivo: {enfoque}.
            Datos: {precio}, {limite}, {canal}.
            Contexto: {detalles}.

            Respuesta ULTRA CONCISA. Máximo 120 palabras. 
            Sin introducciones, sin validación ("excelente idea"), sin teoría.
            
            ESTRUCTURA:
            1. 🧭 DECISIÓN: (La dirección técnica para {nombre}. 1 frase.)
            2. ⚡ HOY: (Acción concreta y única.)
            3. 📅 SECUENCIA: (D1, D3, D5, D7. Una línea por día.)
            4. ✍️ COPY ({canal}): (Texto directo para el cliente final de {negocio}. Usá {precio} y {limite}.)
            5. 🚫 EVITÁ: (El error que rompe la venta.)
            """
            
            try:
                response = model.generate_content(prompt)
                st.divider()
                st.subheader(f"Orden de mando: {nombre}")
                # Usamos st.code para el copy para que sea fácil de copiar
                st.markdown(response.text)
            except Exception as e:
                st.error("Error de conexión.")
