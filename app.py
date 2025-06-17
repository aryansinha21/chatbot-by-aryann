import streamlit as st
import os
import fitz  # PyMuPDF
import docx
import tempfile
from io import StringIO
import requests

# ✅ Must be the first Streamlit command
st.set_page_config(
    page_title="AI Chatbot by Aryann Sinha",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 💬 Title
st.title("🤖 AI Chatbot + File Reader")
st.caption("Made by Aryann Sinha")

# ✅ Get API key from Streamlit secrets
api_key = st.secrets.get("api_key", "")

# 🔄 Normal chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Chat display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 📤 File upload
uploaded_file = st.sidebar.file_uploader("Upload a file (PDF, DOCX, TXT, Image)", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"])

file_text = ""

if uploaded_file:
    file_type = uploaded_file.type
    st.sidebar.write(f"File Type: `{file_type}`")

    if file_type.startswith("image/"):
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.sidebar.info("Image preview shown. No text to extract.")
    elif uploaded_file.name.endswith(".pdf"):
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            file_text = "\n".join([page.get_text() for page in doc])
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        file_text = "\n".join([para.text for para in doc.paragraphs])
    elif uploaded_file.name.endswith(".txt"):
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        file_text = stringio.read()

    if file_text:
        st.sidebar.success("Text extracted from file.")
        st.sidebar.text_area("📄 File Content Preview", file_text, height=200)

# 💬 User input
user_input = st.chat_input("Ask something or start chatting...")

# ✅ Chat logic
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 👇 Prepare prompt (with file content if available)
    prompt = ""
    if file_text:
        prompt += f"Context from file:\n{file_text}\n\n"
    prompt += f"User: {user_input}\nAI:"

    # 🧠 OpenAI or OpenRouter API call
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openchat/openchat-3.5",  # Free model from OpenRouter
        "messages": [
            {"role": "system", "content": "You are a helpful AI chatbot created by Aryann Sinha."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"❌ Error: {e}"

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

