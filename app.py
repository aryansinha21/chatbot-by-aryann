import streamlit as st
import fitz  # PyMuPDF
import docx
from io import StringIO
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="ChatGPT by Aryann Sinha", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

# --- TITLE ---
st.markdown("""
    <h1 style='text-align: center;'>🤖 ChatGPT by Aryann Sinha</h1>
    <p style='text-align: center; font-size: 18px;'>Your personal AI assistant with file upload, image preview, and smart responses</p>
    <hr>
""", unsafe_allow_html=True)

# --- LOAD API KEY FROM SECRETS ---
api_key = st.secrets.get("api_key", "")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- SIDEBAR FILE UPLOAD ---
st.sidebar.header("📁 Upload a File or Image")
file = st.sidebar.file_uploader("Supported: PDF, DOCX, TXT, PNG, JPG", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"])
extracted_text = ""

if file:
    st.sidebar.success(f"Uploaded: {file.name}")
    if file.type.startswith("image"):
        st.image(file, caption=file.name, use_column_width=True)
        st.sidebar.info("Image preview only — not analyzed for text.")
    elif file.name.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        extracted_text = "\n".join([page.get_text() for page in doc])
    elif file.name.endswith(".docx"):
        d = docx.Document(file)
        extracted_text = "\n".join([para.text for para in d.paragraphs])
    else:
        stringio = StringIO(file.getvalue().decode("utf-8"))
        extracted_text = stringio.read()
    if extracted_text:
        st.sidebar.text_area("📄 Extracted Text Preview", extracted_text, height=200)

# --- CHAT INPUT ---
user_input = st.chat_input("Ask me anything...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Combine file text and prompt
    prompt = f"Use the following context to help answer:\n{extracted_text}\n\n{user_input}" if extracted_text else user_input

    # API Call
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openchat/openchat-3.5",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant created by Aryann Sinha."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        reply = res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- FOOTER ---
st.markdown("""
    <hr>
    <p style='text-align: center; color: gray;'>Made with ❤️ by <b>Aryann Sinha</b></p>
""", unsafe_allow_html=True)
