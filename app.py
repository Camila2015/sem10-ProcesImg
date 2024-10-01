import os
import streamlit as st
import base64
from openai import OpenAI

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

st.set_page_config(page_title="Análisis de imagen", layout="centered", initial_sidebar_state="collapsed")
st.title("Análisis de Imagen:🤖🏞️")

# Pregunta inicial
ready_to_start = st.radio("¿Estás listo para empezar?", ("Sí", "No"))

if ready_to_start == "Sí":
    st.markdown("<style>body { background-color: yellow; }</style>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='position: relative; height: 400px; overflow: hidden;'>
            <div class='falling-flowers'>
                <span style='font-size: 30px;'>🌸</span>
                <span style='font-size: 30px;'>🌷</span>
                <span style='font-size: 30px;'>🌼</span>
                <span style='font-size: 30px;'>🌻</span>
                <span style='font-size: 30px;'>🌺</span>
                <span style='font-size: 30px;'>🌸</span>
                <span style='font-size: 30px;'>🌷</span>
                <span style='font-size: 30px;'>🌼</span>
                <span style='font-size: 30px;'>🌻</span>
                <span style='font-size: 30px;'>🌺</span>
            </div>
        </div>
        <style>
            @keyframes fall {
                0% { top: -100%; }
                100% { top: 100%; }
            }
            .falling-flowers {
                position: absolute;
                animation: fall 5s linear infinite;
            }
            .falling-flowers span {
                position: absolute;
                animation: fall 5s linear infinite;
                opacity: 0;
            }
            /* Animar diferentes flores en diferentes tiempos */
            .falling-flowers span:nth-child(1) { left: 10%; animation-delay: 0s; }
            .falling-flowers span:nth-child(2) { left: 20%; animation-delay: 1s; }
            .falling-flowers span:nth-child(3) { left: 30%; animation-delay: 2s; }
            .falling-flowers span:nth-child(4) { left: 40%; animation-delay: 3s; }
            .falling-flowers span:nth-child(5) { left: 50%; animation-delay: 4s; }
            .falling-flowers span:nth-child(6) { left: 60%; animation-delay: 0s; }
            .falling-flowers span:nth-child(7) { left: 70%; animation-delay: 1s; }
            .falling-flowers span:nth-child(8) { left: 80%; animation-delay: 2s; }
            .falling-flowers span:nth-child(9) { left: 90%; animation-delay: 3s; }
            .falling-flowers span:nth-child(10) { left: 50%; animation-delay: 4s; }
        </style>
        """, unsafe_allow_html=True
    )
elif ready_to_start == "No":
    st.warning("¡No te preocupes! Puedes regresar cuando estés listo.")

ke = st.text_input('Ingresa tu Clave')
os.environ['OPENAI_API_KEY'] = ke

api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("Image", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)

show_details = st.toggle("Adiciona detalles sobre la imagen", value=False)

if show_details:
    additional_details = st.text_area(
        "Adiciona contexto de la imagen aquí:",
        disabled=not show_details
    )

analyze_button = st.button("Analiza la imagen", type="secondary")

if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("Analizando ..."):
        base64_image = encode_image(uploaded_file)
        prompt_text = "Describe lo que ves en la imagen en español"
    
        if show_details and additional_details:
            prompt_text += (
                f"\n\nContexto adicional proporcionado por el usuario:\n{additional_details}"
            )
    
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ]
    
        try:
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4-vision-preview", messages=messages,   
                max_tokens=1200, stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    if not uploaded_file and analyze_button:
        st.warning("Please upload an image.")
    if not api_key:
        st.warning("Por favor ingresa tu API key.")


