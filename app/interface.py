# app/interface.py

import streamlit as st
from retriever import DocumentRetriever
from utils import load_and_chunk_document
import requests

# Ollama model config
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

# Set page config
st.set_page_config(page_title="Chat with Document", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("📄 Chat with your PDF using Ollama + ChromaDB")

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

        prompt = f"Answer the following question based on the context.\n\nContext:\n{context_text}\n\nQuestion: {user_input}"

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

    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
