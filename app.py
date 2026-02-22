import streamlit as st
import google.generativeai as genai

# 1. Configuración de página y estilo
st.set_page_config(page_title="SPRING UNLOCK 🧭", layout="centered")

# Estilo personalizado para evitar párrafos densos
st.markdown("""
    <style>
    .stAlert p { font-size: 16px; font-weight: 400; }
    .main { max-width: 800px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CREDENCIALES (BARRA LATERAL) ---
with st.sidebar:
    api_key = st.text_input("Ingresa tu Google API Key:", type="password")
    if api_key:
        # Inicializamos el cliente nativo de Google (sin LangChain)
        client = genai.Client(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("Error de configuración de API. Revisá tus Secrets.")
    st.stop()

# 3. Interfaz de usuario (Brújula)
st.title("🧭 SPRING UNLOCK")
st.write("De la nube de ideas al mapa de hoy.")

with st.form("diagnostico_form"):
    nombre = st.text_input("¿Cómo te llamás?", placeholder="Tu nombre")
    negocio = st.text_input("¿De qué es tu negocio?", placeholder="Ej: Centro de Pilates")
    caos = st.text_area("¿Qué tenés en la cabeza? (quiero lanzar una promo, tengo deudas, no sé qué publicar...)", 
                        placeholder="Mientras más info, mejor puedo ayudarte...")
    
    boton = st.form_submit_button("Calibrar mi Brújula 🚀")

# 4. Lógica de generación
def generar_respuesta(nombre, negocio, caos):
    # System Prompt optimizado para evitar "muros de texto" y ser empático
    prompt_sistema = f"""
    Actuá como una socia estratégica de la Agencia Spring. Tu cliente es {nombre}, que tiene un negocio de {negocio}.
    Está abrumada y necesita ORDEN. 
    
    REGLAS ESTRICTAS DE FORMATO:
    1. Usá lenguaje humano, cercano y empático. Nada de términos corporativos fríos.
    2. Prohibido escribir párrafos de más de 3 líneas.
    3. Usá Emojis para guiar la lectura.
    4. Estructura la respuesta exactamente así:
       - Un saludo cálido por su nombre.
       - SECCIÓN: ⚡ EL MOVIMIENTO DE HOY (La acción que trae dinero o calma inmediata).
       - SECCIÓN: 📋 HOJA DE RUTA (Máximo 4 bullet points cortos).
       - SECCIÓN: 📦 CAJÓN DE IDEAS (Guardá acá lo que la distrae hoy para que lo haga después).
       - SECCIÓN: ⚠️ CUIDADO ACÁ (El error que debe evitar).

    TEXTO A PROCESAR: {caos}
    """
    
    try:
        response = model.generate_content(prompt_sistema)
        return response.text
    except Exception as e:
        return f"Ups! Algo falló en la conexión: {str(e)}"

# 5. Ejecución y Visualización
if boton:
    if not nombre or not caos:
        st.warning("Por favor, completá tu nombre y contame qué te pasa para poder ayudarte.")
    else:
        with st.spinner("Limpiando el parabrisas..."):
            resultado = generar_respuesta(nombre, negocio, caos)
            
            st.divider()
            # Mostramos el resultado de forma organizada
            st.markdown(resultado)
            
            st.balloons()
            st.info("¿Este plan te da un poco de paz? Enfocate en el Movimiento de Hoy.")

# 6. Footer
st.caption("Hecho con ❤️ por Agencia Spring + IA")
