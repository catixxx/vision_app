import os
import streamlit as st
import base64
from openai import OpenAI

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="✨ Análisis de Imagen",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- ESTILO PERSONALIZADO ---
st.markdown("""
<style>
/* Fondo en degradado suave */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #fff0f6 0%, #fce4ec 100%);
}

/* Encabezado */
h1 {
    text-align: center;
    color: #b14d75;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
}

/* Cajas y botones */
div.stButton > button {
    background-color: #f7b5cd;
    color: white;
    border-radius: 15px;
    padding: 0.6em 1.2em;
    font-size: 1.1em;
    border: none;
    transition: all 0.3s ease-in-out;
}

div.stButton > button:hover {
    background-color: #e48fb1;
    transform: scale(1.05);
}

/* Campos de texto */
input, textarea {
    border-radius: 10px !important;
    border: 1px solid #f3a7c3 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #ffe4ee !important;
    color: #b14d75 !important;
    font-weight: 600;
}

/* Spinner */
[data-testid="stSpinner"] {
    color: #b14d75;
}

/* Mensajes */
.stAlert {
    border-radius: 12px;
}

/* Fuente general */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# --- TÍTULO PRINCIPAL ---
st.title("🌷 Análisis de Imagen con IA 🤖")

# --- INGRESO DE CLAVE ---
st.markdown("<h4 style='color:#b14d75;'>🔑 Ingresa tu clave de acceso</h4>", unsafe_allow_html=True)
ke = st.text_input('', type='password', placeholder="Escribe aquí tu clave de OpenAI")
os.environ['OPENAI_API_KEY'] = ke

api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# --- SUBIR IMAGEN ---
st.markdown("<h4 style='color:#b14d75;'>📸 Sube una imagen para analizar</h4>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Selecciona un archivo (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with st.expander("🌼 Vista previa de la imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# --- DETALLES ADICIONALES ---
show_details = st.toggle("✨ Agregar detalles adicionales", value=False)

if show_details:
    additional_details = st.text_area(
        "🪷 Describe brevemente el contexto de la imagen:",
        placeholder="Ejemplo: Esta foto fue tomada durante un paseo por el bosque...",
    )

# --- BOTÓN DE ANÁLISIS ---
analyze_button = st.button("🌈 Analizar Imagen")

# --- FUNCIÓN PARA ENCODEAR IMAGEN ---
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# --- LÓGICA DE ANÁLISIS ---
if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("Analizando con amor y precisión 💭..."):
        base64_image = encode_image(uploaded_file)
        prompt_text = "Describe con detalle y en español lo que observas en esta imagen."

        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional proporcionado por el usuario:\n{additional_details}"

        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_text},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ],
        }]

        try:
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4o", messages=messages, max_tokens=1200, stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(f"<div style='color:#7a3b59; font-size:1.1em;'>{full_response}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

else:
    if not uploaded_file and analyze_button:
        st.warning("🌻 Por favor, sube una imagen antes de analizar.")
    if not api_key:
        st.warning("🌷 Ingresa tu API key para continuar.")
