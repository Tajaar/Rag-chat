# retriever.py

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

class DocumentRetriever:
    def __init__(self, persist_directory="./chroma_db", model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.embedding_function = SentenceTransformerEmbeddingFunction(model_name=self.model_name)
        self.collection = self._init_collection()

    def _init_collection(self):
        try:
            return self.client.get_collection(name="document_chunks")
        except:
            return self.client.create_collection(
                name="document_chunks",
                embedding_function=self.embedding_function
            )

    def add_documents(self, chunks):
        """
        Add list of chunks to ChromaDB
        chunks: List[Dict] with "id", "text", and optional "metadata"
        """
        ids = [chunk["id"] for chunk in chunks]
        texts = [chunk["text"] for chunk in chunks]

        # Ensure metadata is non-empty
        metadatas = []
        for chunk in chunks:
            metadata = chunk.get("metadata")
            if not metadata:
                metadata = {"source": "unknown"}  # or any default key-value pair
            metadatas.append(metadata)

        self.collection.add(documents=texts, ids=ids, metadatas=metadatas)

    def retrieve(self, query, top_k=3):
        """
        Return top_k most relevant chunks for a given query
        """
        results = self.collection.query(query_texts=[query], n_results=top_k)
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        return documents, metadatas



    def reset(self):
        """
        Reset collection (for reloading new docs)
        """
        self.client.delete_collection(name="document_chunks")
        self.collection = self.client.create_collection(
            name="document_chunks",
            embedding_function=self.embedding_function
        )
