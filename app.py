import streamlit as st
import requests
import os
from PIL import Image

# --- Page config (MUST BE FIRST) ---
st.set_page_config(page_title="ChatGPT by Aryann Sinha", page_icon="🤖", layout="centered")

# --- Title ---
st.markdown("""
<h1 style='text-align: center;'>🤖 ChatGPT by Aryann Sinha</h1>
<p style='text-align: center;'>Your personal AI assistant with file upload, image preview, and smart responses</p>
""", unsafe_allow_html=True)

# --- API key (stored in .streamlit/secrets.toml) ---
API_KEY = st.secrets["api_key"]

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat History Display ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a file (image or text)", type=["png", "jpg", "jpeg", "txt", "pdf"])
if uploaded_file:
    file_details = f"**Uploaded:** {uploaded_file.name} ({round(uploaded_file.size / 1024, 2)} KB)"
    st.markdown(file_details)

    if uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption=uploaded_file.name)
    elif uploaded_file.type.endswith("text/plain"):
        text_content = uploaded_file.read().decode("utf-8")
        st.text_area("File Content", text_content, height=200)

# --- User Input ---
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Add user input to chat
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare OpenRouter request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-70b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            *st.session_state.messages
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "⚠️ Sorry, no response from the model."

    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- Footer ---
st.markdown("""
<hr style='margin-top: 2rem;'>
<p style='text-align: center;'>Made with ❤️ by <strong>Aryann Sinha</strong></p>
""", unsafe_allow_html=True)
