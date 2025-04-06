# app/interface.py

import streamlit as st
from retriever import DocumentRetriever
from utils import load_and_chunk_document
import requests
import os
import json
import uuid

# Ollama model config
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

# Chat history folder
CHAT_HISTORY_DIR = "chat_histories"
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)
# Set page config
st.set_page_config(page_title="Chat with Document", layout="wide")

# Custom CSS styling
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: white;
        }
        .block-container {
            background-color: transparent;
        }
        .stChatMessage.user div {
            background-color: #005f73;
            color: white;
            padding: 12px;
            border-radius: 10px;
        }
        .stChatMessage.assistant div {
            background-color: #0a9396;
            color: white;
            padding: 12px;
            border-radius: 10px;
        }
        .stButton>button, .stTextInput>div>input {
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
        }
        .stFileUploader>div>div>button {
            border-radius: 10px;
            padding: 10px;
            background-color: #94d2bd;
            color: black;
        }
        .stSpinner>div>div>div>div {
            color: white;
        }
        .css-18e3th9 {
            background-color: #001219 !important;
        }
        .css-1d391kg {
            background-color: #001219 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar - Rename chat session
st.sidebar.title("💬 Chat Session")

# Get existing session ID or create new
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.session_name = "Untitled Chat"
    st.session_state.messages = []

# Rename input field
new_name = st.sidebar.text_input("Session Name", value=st.session_state.session_name)
if new_name != st.session_state.session_name:
    # Rename chat file
    old_path = os.path.join(CHAT_HISTORY_DIR, f"{st.session_state.session_id}.json")
    new_path = os.path.join(CHAT_HISTORY_DIR, f"{new_name}.json")
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
    st.session_state.session_name = new_name
    st.session_state.session_id = new_name

# Option to delete current chat
if st.sidebar.button("🗑️ Delete Chat"):
    try:
        os.remove(os.path.join(CHAT_HISTORY_DIR, f"{st.session_state.session_id}.json"))
        st.sidebar.success("Chat deleted. Reloading...")
        st.session_state.clear()
        st.rerun()
    except:
        st.sidebar.error("Failed to delete chat.")

st.title("📄 Chat with your PDF using AI")

# --- Load existing chat sessions ---
def load_existing_sessions():
    sessions = []
    for file in os.listdir(CHAT_HISTORY_DIR):
        if file.endswith(".json"):
            session_id = file.replace(".json", "")
            with open(os.path.join(CHAT_HISTORY_DIR, file), "r", encoding="utf-8") as f:
                messages = json.load(f)
            # First assistant or user message as preview (if exists)
            preview = next((m["content"] for m in messages if m["role"] == "user"), "No preview")
            sessions.append((session_id, preview))
    return sessions

existing_sessions = load_existing_sessions()

# Show session list if any
if existing_sessions:
    st.sidebar.subheader("📁 Load Previous Chat")
    session_options = [f"{name} - {preview[:30]}..." for name, preview in existing_sessions]
    selected = st.sidebar.selectbox("Select Session", [""] + session_options)

    if selected and "session_id" in st.session_state:
        selected_id = selected.split(" - ")[0]
        if selected_id != st.session_state.session_id:
            # Load selected chat
            with open(os.path.join(CHAT_HISTORY_DIR, f"{selected_id}.json"), "r") as f:
                st.session_state.messages = json.load(f)
            st.session_state.session_id = selected_id
            st.session_state.session_name = selected_id
            st.rerun()

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading and chunking document..."):
        chunks = load_and_chunk_document(uploaded_file)
        retriever = DocumentRetriever()
        retriever.reset()
        retriever.add_documents(chunks)
        st.success("Document loaded and indexed!")

    # Chat UI
    user_input = st.chat_input("Ask a question about the document...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Retrieving context..."):
            documents, metadatas = retriever.retrieve(user_input, top_k=3)
            context = "\n".join(documents) if documents else ""
            context_text = "\n\n".join(context)

        prompt = (
            f"You are a helpful assistant. Structure your response with bullet points or a table if applicable. Answer only from the context of the document.\n\n"
            f"\n\nContext:\n{context_text}\n\nQuestion: {user_input}"
        )

        with st.spinner("Generating response..."):
            response = requests.post(OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            })

            if response.status_code == 200:
                answer = response.json()["response"].strip()
            else:
                answer = "❌ Error generating response from Ollama."

        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Save chat
        with open(os.path.join(CHAT_HISTORY_DIR, f"{st.session_state.session_id}.json"), "w") as f:
            json.dump(st.session_state.messages, f, indent=2)

# Display chat messages
for msg in st.session_state.get("messages", []):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
