import streamlit as st
import google.generativeai as genai

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="SPRING UNLOCK 🧭", page_icon="🧭", layout="centered")

# ---------------------------
# SIDEBAR - API KEY
# ---------------------------
with st.sidebar:
    st.title("Configuración")
    user_api_key = st.text_input("Ingresá tu Google API Key", type="password")

# ---------------------------
# GATE: API KEY REQUIRED
# ---------------------------
if not user_api_key:
    st.title("🧭 SPRING UNLOCK")
    st.subheader("Tu GPS con criterio.")
    st.write("Ingresá tu API Key en la barra lateral para empezar.")
    st.stop()

# Configure Gemini
genai.configure(api_key=user_api_key)

# Model
MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# ---------------------------
# UI
# ---------------------------
st.title("🧭 SPRING UNLOCK")
st.write("Criterio estratégico para ejecutar HOY.")

with st.form("spring_form"):
    nombre = st.text_input("¿Cómo te llamás?", placeholder="Laura")
    negocio = st.text_input("¿De qué es tu negocio?", placeholder="Centro de Pilates")
    enfoque = st.text_input("¿En qué una cosa nos enfocamos hoy?", placeholder="Lanzar promo San Valentín")
    detalles = st.text_area(
        "Contame el nudo de la cuestión:",
        placeholder="Tengo la idea pero me trabo en cómo comunicarla. Estoy posteando poco, no sé qué decir y quiero que la promo se entienda rápido.",
        height=140,
    )

    col1, col2 = st.columns(2)
    with col1:
        precio = st.text_input("Precio (opcional)", placeholder="Ej: 2 clases x $...")
    with col2:
        vigencia = st.text_input("Vigencia / fecha límite (opcional)", placeholder="Ej: hasta el 14/02")

    canal = st.selectbox(
        "Canal principal",
        ["Instagram", "WhatsApp", "Instagram + WhatsApp", "Otro"],
        index=2,
    )

    submit = st.form_submit_button("Calibrar Brújula 🚀")

# ---------------------------
# PROMPT BUILDER
# ---------------------------
def build_prompt(nombre: str, negocio: str, enfoque: str, detalles: str, precio: str, vigencia: str, canal: str) -> str:
    precio_txt = precio.strip() if precio else ""
    vigencia_txt = vigencia.strip() if vigencia else ""

    extra = []
    if precio_txt:
        extra.append(f"Precio indicado: {precio_txt}.")
    if vigencia_txt:
        extra.append(f"Vigencia indicada: {vigencia_txt}.")
    extra.append(f"Canal principal: {canal}.")

    extra_block = " ".join(extra)

    return f"""
Actuá como socia estratégica de Agencia Spring.
Cliente: {nombre}. Negocio: {negocio}.
Foco de hoy: {enfoque}.
Nudo real: {detalles}
{extra_block}

REGLAS (obligatorias):
- No des clases ni contexto general (no expliques fechas ni teoría).
- Usá datos del caso (nombre, negocio, foco y nudo) de forma explícita. Si no los usás, la respuesta no sirve.
- Total máximo: 220 palabras.
- Español neutro, tono profesional-cercano, directo y protector.
- Cero relleno. Cero motivación vacía.

FORMATO EXACTO:

1) 🧭 CRITERIO (máx 60 palabras)
2–3 frases: qué está bien + qué falta + qué decidimos hoy.

2) ⚡ MOVIMIENTO DE HOY (tabla)
| Qué hacés hoy | Para qué sirve |
Incluí 3 filas máximo. Acciones atómicas.

3) ✍️ COPY LISTO (un solo bloque)
Un texto corto listo para {canal} (máx 70 palabras). Debe incluir CTA claro.
Si hay precio o vigencia, intégralos sin inventar.

4) 📆 SECUENCIA 7 DÍAS (solo 4 líneas)
D1:
D3:
D5:
D7:

5) 🚫 LÍMITE (una sola frase)
Qué NO hacer hoy para no arruinar el lanzamiento.
""".strip()

# ---------------------------
# GENERATION
# ---------------------------
if submit:
    nombre = (nombre or "").strip()
    negocio = (negocio or "").strip()
    enfoque = (enfoque or "").strip()
    detalles = (detalles or "").strip()

    if not nombre or not enfoque or not detalles:
        st.warning("Completá nombre, enfoque y nudo para darte una dirección clara.")
        st.stop()

    with st.spinner("Analizando con criterio Spring..."):
        prompt = build_prompt(nombre, negocio, enfoque, detalles, precio, vigencia, canal)

        try:
            response = model.generate_content(prompt)
            text = (response.text or "").strip()

            if not text:
                st.error("No recibí una respuesta. Probá de nuevo.")
                st.stop()

            st.divider()
            st.header(f"Norte estratégico: {nombre}")
            st.markdown(text)

            st.divider()
            st.download_button(
                "Descargar plan",
                text,
                file_name=f"Plan_Spring_{nombre}.txt",
                mime="text/plain",
            )

        except Exception:
            st.error("Error con la API. Verificá tu llave e intentá de nuevo.")
