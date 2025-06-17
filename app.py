# app.py
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# --- Page config (MUST BE FIRST) ---
st.set_page_config(page_title="ChatGPT by Aryann Sinha", page_icon="🤖", layout="centered")

# --- Title ---
st.markdown("""
<h1 style='text-align: center;'>🤖 ChatGPT by Aryann Sinha</h1>
<p style='text-align: center;'>Your personal AI assistant with file upload, image preview, and smart responses</p>
""", unsafe_allow_html=True)

# --- Load API key from secrets ---
api_key = st.secrets["api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- File uploader ---
uploaded_file = st.file_uploader("Upload a file (image or text)", type=["png", "jpg", "jpeg", "txt"])
if uploaded_file:
    st.markdown(f"**Uploaded:** {uploaded_file.name} ({round(uploaded_file.size / 1024, 2)} KB)")
    if uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption=uploaded_file.name)
    elif uploaded_file.type.endswith("plain"):
        text_content = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", text_content, height=200)

# --- Chat input ---
prompt = st.chat_input("Ask me anything...")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = model.generate_content(prompt)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- Footer ---
st.markdown("""
<hr style='margin-top: 2rem;'>
<p style='text-align: center;'>Made with ❤️ by <strong>Aryann Sinha</strong></p>
""", unsafe_allow_html=True)
