import streamlit as st
import google.generativeai as genai

# Configuración de estética y legibilidad
st.set_page_config(page_title="SPRING UNLOCK 🧭", layout="centered")

# Sidebar para la API Key
with st.sidebar:
    st.title("Configuración")
    user_api_key = st.text_input("Ingresá tu Google API Key", type="password")
    st.divider()

if not user_api_key:
    st.title("🧭 SPRING UNLOCK")
    st.subheader("Tu GPS para dejar de dar vueltas.")
    st.write("Ingresá tu API Key en la barra lateral para calibrar tu brújula.")
    st.stop()

# Inicialización
genai.configure(api_key=user_api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# Interfaz limpia
st.title("🧭 SPRING UNLOCK")
st.write("Elegí un Norte. Ejecutemos hoy.")

with st.form("spring_form"):
    nombre = st.text_input("Bienvenid@¿Cómo te llamás?", placeholder="Tu nombre")
    negocio = st.text_input("¿De qué es tu negocio?", placeholder="Ej: Centro de Pilates")
    
    # El cambio clave: Enfoque en una sola cosa
    caos = st.text_area("Enfocáte en UNA cosa que quieras resolver hoy:", 
                        placeholder="Ej: Lanzar una promo, organizar mis ideas, no sé qué publicar...")
    
    submit = st.form_submit_button("Calibrar mi Brújula 🚀")

if submit:
    if not nombre or not caos:
        st.warning("Completá los campos para que pueda darte una dirección clara.")
    else:
        with st.spinner("Analizando tu prioridad..."):
            
            prompt = f"""
            Actuá como la socia estratégica de la Agencia Spring. Tu cliente es {nombre} y tiene un negocio de {negocio}.
            Se quiere enfocar exclusivamente en esto hoy: "{caos}".
            
            Tu objetivo es dar una respuesta PROFUNDA, ÚTIL y ACCIONABLE sobre ese tema específico.
            
            ESTRUCTURA DE RESPUESTA:
            1. 🧭 EL NORTE PARA {nombre.upper()}: Validá su idea de forma cálida pero analítica. Decile por qué esa 'una cosa' es importante ahora.
            
            2. ⚡ EL MOVIMIENTO DE HOY: La acción exacta, paso a paso, para ejecutar eso que quiere resolver. Sé muy específica.
            
            3. 🛠️ KIT DE HERRAMIENTAS: Si es contenido, dale 3 ganchos (hooks). Si es una promo, sugerile el precio o la mecánica. Si es organización, dale los 3 primeros pasos.
            
            4. 🧠 POR QUÉ ESTO FUNCIONA: Explicación estratégica simple de por qué este movimiento le sirve a su negocio de {negocio}.
            
            5. ⚠️ EL PELIGRO: Qué es lo único que NO debe hacer para no arruinar este movimiento.

            TONO: Empático, senior pero simple, motivador y muy ordenado. Nada de párrafos gigantes.
            """
            
            try:
                response = model.generate_content(prompt)
                
                st.divider()
                st.subheader(f"Reporte de Acción: {nombre}")
                
                # Output visualmente organizado
                st.markdown(response.text)
                
                st.divider()
                st.download_button("Guardar Hoja de Ruta", response.text, file_name="mi_norte_spring.txt")
                st.balloons()
                
            except Exception as e:
                st.error("Hubo un error con la API. Revisá que sea válida.")
                st.caption(f"Detalle técnico: {e}")

st.caption("Agencia Spring | Brújula Operativa")
