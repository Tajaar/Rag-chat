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

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot
```

### 2. Create a Virtual Environment and Install Dependencies

Using Conda:

```bash
conda create -n local-rag python=3.10 -y
conda activate local-rag
pip install -r requirements.txt
```

---

## 🧠 Ollama Setup

Install Ollama from [https://ollama.com](https://ollama.com).

Then run the model:

```bash
ollama run mistral
```

Make sure the Ollama server is running before launching the app.

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
EMBEDDING_MODEL=all-MiniLM-L6-v2
PERSIST_DIRECTORY=./chroma_db
```

---

## ▶️ Running the App

```bash
streamlit run app/interface.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

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
