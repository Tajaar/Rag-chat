# utils.py

import os
from typing import List, Dict
import uuid
from uuid import uuid4
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdf(file_path: str) -> str:
    """
    Load and extract text from a PDF using PyMuPDF.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

def load_txt(file_path: str) -> str:
    """
    Load plain text from a .txt file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def split_text_into_chunks(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict]:
    """
    Split text into overlapping chunks and return with unique IDs.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " "]
    )

    chunks = splitter.split_text(text)
    return [{"id": str(uuid4()), "text": chunk} for chunk in chunks]

def load_and_chunk_document(file, chunk_size=300):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    chunks = []
    words = text.split()
    for i in range(0, len(words), chunk_size):
        chunk_text = " ".join(words[i:i+chunk_size])
        chunk_id = str(uuid.uuid4())
        chunks.append({"id": chunk_id, "text": chunk_text, "metadata": {"source": "uploaded"}})

    return chunks
