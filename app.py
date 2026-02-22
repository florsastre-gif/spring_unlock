import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="SPRING UNLOCK",
    page_icon="⚙️",
    layout="centered"
)

# ---------------------------
# SIDEBAR - API KEY
# ---------------------------

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Google API Key", type="password")
    st.caption("Tu clave no se guarda. Solo se usa en esta sesión.")

if api_key:
    genai.configure(api_key=api_key)

# ---------------------------
# HEADER
# ---------------------------

st.title("🔓 SPRING UNLOCK")
st.subheader("Lanzá y activá sin dispersión.")


st.divider()

# ---------------------------
# FORM
# ---------------------------

with st.form("spring_unlock_form"):

    objetivo = st.selectbox(
        "¿Qué querés lanzar ahora?",
        [
            "Comunicar una promo",
            "Lanzar un servicio nuevo",
            "Reactivar ventas",
            "Ordenar contenido para vender mejor"
        ]
    )

    oferta = st.selectbox(
        "¿Tu oferta está clara y con precio definido?",
        [
            "Sí, lista para vender",
            "Más o menos",
            "No, todavía la estoy armando"
        ]
    )

    mensaje = st.selectbox(
        "¿Tu mensaje principal está definido?",
        [
            "Sí, lo puedo decir en una frase",
            "Más o menos",
            "No"
        ]
    )

    frecuencia = st.selectbox(
        "¿Con qué frecuencia estás publicando hoy?",
        [
            "Constante",
            "Irregular",
            "Casi nunca"
        ]
    )

    base_clientes = st.selectbox(
        "¿Tenés base de clientes o contactos?",
        [
            "Sí, activa",
            "Sí, pero inactiva",
            "No"
        ]
    )

    contexto_extra = st.text_area(
        "Si querés, contame en una o dos líneas qué está pasando ahora:"
    )

    submitted = st.form_submit_button("UNLOCK")

# ---------------------------
# GENERATION
# ---------------------------

def generar_respuesta(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

if submitted:

    if not api_key:
        st.warning("Necesitás ingresar tu Google API Key.")
    else:

        with st.spinner("Procesando tu estrategia..."):

            prompt = f"""
Actuá como una estratega senior de marketing.

Tu tono debe ser:
- Clínico en el análisis
- Protector en la entrega
- Claro, directo, sin frases motivacionales vacías
- Sin tecnicismos innecesarios

El usuario quiere activar o lanzar algo.

Información actual:

Objetivo: {objetivo}
Oferta definida: {oferta}
Mensaje claro: {mensaje}
Frecuencia de publicación: {frecuencia}
Base de clientes: {base_clientes}
Contexto adicional: {contexto_extra}

Devolvé la respuesta con esta estructura EXACTA:

🔎 ESTADO OPERATIVO ACTUAL:
Breve diagnóstico claro y directo.

🎯 SECUENCIA RECOMENDADA (orden obligatorio):
Paso 1:
Paso 2:
Paso 3:
Paso 4 (si aplica):

📅 PLAN DE 7 DÍAS:
Día 1:
Día 2:
Día 3:
Día 4:
Día 5:
Día 6:
Día 7:

⚠️ ERROR TÍPICO A EVITAR:
Un solo error común según su estado.

No des más de lo pedido.
No des teoría.
Solo orden táctico ejecutable.
"""

            resultado = generar_respuesta(prompt)

        st.divider()
        st.markdown(resultado)
