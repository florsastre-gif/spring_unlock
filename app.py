import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SPRING UNLOCK 🧭", layout="centered")

with st.sidebar:
    st.title("Configuración")
    user_api_key = st.text_input("Ingresá tu Google API Key", type="password")
    st.info("Obtené tu llave en [Google AI Studio](https://aistudio.google.com/app/apikey)")

if not user_api_key:
    st.title("🧭 SPRING UNLOCK")
    st.info("Configurá tu API Key en la barra lateral para activar la brújula.")
    st.stop()

genai.configure(api_key=user_api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🧭 SPRING UNLOCK")

with st.form("spring_form"):
    nombre = st.text_input("Nombre", placeholder="Laura")
    negocio = st.text_input("Negocio", placeholder="Centro de Pilates")
    enfoque = st.text_input("¿Qué activamos hoy?", placeholder="Promo San Valentín")
    
    col1, col2, col3 = st.columns(3)
    with col1: precio = st.text_input("Precio", placeholder="$15.000")
    with col2: limite = st.text_input("Límite", placeholder="Viernes")
    with col3: canal = st.selectbox("Canal", ["WhatsApp", "Instagram"])
    
    detalles = st.text_area("Contexto (caos/idea):", placeholder="Contame qué te traba...")
    submit = st.form_submit_button("Calibrar Brújula 🚀")

if submit:
    if not nombre or not detalles:
        st.warning("Faltan datos para procesar.")
    else:
        with st.spinner("Decidiendo ruta..."):
            # PROMPT HÍBRIDO: Ejecución dura + Guía técnica
            prompt = f"""
            Actuá como estratega senior de ejecución (marketing táctico).
            Cliente: {nombre}
            Negocio: {negocio}
            Objetivo de hoy: {enfoque}

            Datos (NO inventar):
            - precio: {precio if precio else "SIN DATO"}
            - limite: {limite if limite else "SIN DATO"}
            - canal: {canal}

            Contexto real:
            {detalles}

            REGLAS DURAS:
            - Respuesta ultra concisa (máx 160 palabras).
            - Sin introducciones. Sin validación. Sin teoría. Sin “por qué funciona”.
            - No inventes datos. Si precio o limite es SIN DATO, NO lo menciones en el copy.
            - Formato obligatorio: respetá exactamente los encabezados y el orden.
            - Cada línea de SECUENCIA debe empezar EXACTAMENTE con D1:, D3:, D5:, D7:
            - El COPY debe ir entre delimitadores para copiar fácil.

            FORMATO (EXACTO):

            🧭 DECISIÓN:
            (1 frase técnica y concreta que resuelva el nudo de {nombre})

            ⚡ HOY:
            (1 acción única, atómica y prioritaria)

            📅 SECUENCIA:
            D1:
            D3:
            D5:
            D7:

            ✍️ COPY ({canal}):
            COPY_START
            (2–3 frases. 1 CTA. Hablale al cliente de {negocio}, no a la dueña.)
            COPY_END

            🚫 EVITÁ:
            (1 frase sobre el error técnico que rompe este plan)
            """
            
            try:
                response = model.generate_content(prompt)
                st.divider()
                st.subheader(f"Norte de ejecución: {nombre}")
                
                # Renderizado limpio del resultado
                st.markdown(response.text)
                
                st.divider()
                st.download_button("Descargar Plan", response.text, file_name=f"Spring_{nombre}.txt")
                
            except Exception as e:
                st.error(f"Error técnico: {str(e)}")

st.caption("Agencia Spring | Estrategia Aplicada 2026")
