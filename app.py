import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page config
st.set_page_config(page_title="Gemini Chatbot by Aryann Sinha", page_icon="🤖")

# Load API key
genai.configure(api_key=st.secrets["api_key"])

# Initialize Gemini Pro model
model = genai.GenerativeModel(model_name="models/gemini-pro")

# Title
st.markdown("<h1 style='text-align: center;'>🤖 Gemini Chatbot by Aryann Sinha</h1>", unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader("Upload a file (image or text)", type=["png", "jpg", "jpeg", "txt"])
if uploaded_file:
    st.markdown(f"**Uploaded:** {uploaded_file.name}")
    if uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
    elif uploaded_file.type == "text/plain":
        text_content = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", value=text_content, height=200)

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
prompt = st.chat_input("Ask me anything...")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "parts": [prompt]})

    try:
        response = model.generate_content(st.session_state.chat_history)
        reply = response.text
        st.chat_message("assistant").markdown(reply)
        st.session_state.chat_history.append({"role": "model", "parts": [reply]})
    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# Footer
st.markdown("<hr><p style='text-align: center;'>Made with ❤️ by <strong>Aryann Sinha</strong></p>", unsafe_allow_html=True)
