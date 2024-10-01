import os
import streamlit as st
import base64
from openai import OpenAI

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

st.set_page_config(page_title="Analisis de imagen", layout="centered", initial_sidebar_state="collapsed")
st.image("analisis.png", caption="Análisis de Imagen", use_column_width=True, width=800)

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
    additional_details = st.text_area("Adiciona contexto de la imagen aqui:", disabled=not show_details)

analyze_button = st.button("Analiza la imagen", type="secondary")

if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("Analizando ..."):
        base64_image = encode_image(uploaded_file)
        prompt_text = ("Describe what you see in the image in spanish")

        if show_details and additional_details:
            prompt_text += f"\n\nAdditional Context Provided by the User:\n{additional_details}"

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


