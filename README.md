# RAG-based Document Chatbot

This project is a Retrieval-Augmented Generation (RAG) based chatbot that allows you to upload a PDF and interact with it conversationally. The system retrieves semantically relevant document chunks using ChromaDB and generates contextual answers using a local LLM via Ollama.

---

## 🚀 Features

- Upload and chat with your own PDF documents
- Semantic document search using ChromaDB
- Fast and lightweight local LLM response via Ollama
- Conversational chat interface built with Streamlit
- Persistent vector store with SentenceTransformer embeddings

---

## 🗂️ Project Structure

```
Rag-chat/
├── app/
│   ├── interface.py          # Streamlit UI interface
│   ├── retriever.py          # ChromaDB-based document retrieval logic
│   └── utils.py              # PDF processing utilities
├── uploaded_docs/            # Folder to store uploaded PDFs
├── chroma_db/                # Persistent Chroma vector storage
├── .env                      # Environment variables
├── .gitignore                # Ignored files and folders
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview
```

---

### 🛠️ Project Execution Steps

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot
```

2. **📦 Environment Setup**
   - Create a new Python environment using Anaconda or `venv`.
   - Install required dependencies using `pip`:
     ```bash
     pip install -r requirements.txt
     ```

3. **🚀 Start Ollama**
   - Make sure [Ollama](https://ollama.com) is installed.
   - Pull and start the model (e.g., Llama 3):
     ```bash
     ollama pull llama3
     ollama serve
     ```
     
4. **📁 Directory Setup**
   Ensure the following structure is present:
   ```
   project/
   ├── app/
   │   ├── interface.py
   │   └── retriever.py
   ├── utils.py
   ├── chat_histories/
   ├── requirements.txt
   ```

5. **💬 Run the Streamlit App**
   - From the project root, launch the app:
     ```bash
     streamlit run app/interface.py
     ```

6. **📄 Upload Document & Chat**
   - Use the web interface to upload a PDF.
   - Ask questions about the content and receive structured responses.

7. **💾 Save & Rename Chats**
   - Use the sidebar to rename or delete chat sessions.
   - Chats are saved as `.json` files under the `chat_histories/` directory.

8. **📌 Notes**
   - Ensure Ollama is running before starting the app.
   - If you face module import issues, run Streamlit from the **project root**:
     ```bash
     cd project
     streamlit run app/interface.py
     ```
---

## ⚙️ How It Works

1. Upload a PDF document.
2. The file is split into text chunks.
3. Each chunk is embedded and stored in ChromaDB.
4. When you ask a question, the most relevant chunks are retrieved.
5. The context is passed to the Ollama-powered LLM, which generates a response.
6. The full interaction happens in a chat interface.

---

## 🧰 Tech Stack

- **Streamlit** — Web interface
- **ChromaDB** — Vector database
- **SentenceTransformers** — Text embedding
- **Ollama** — Local LLM inference
- **PyMuPDF** (`fitz`) — PDF text extraction

---
