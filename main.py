# main.py

from app.retriever import DocumentRetriever
from app.generator import ResponseGenerator
from app.utils import load_and_chunk_document

def main():
    print("\n📄 Welcome to the RAG-based Document Chatbot (CLI Mode)")
    file_path = input("Enter path to your PDF or TXT document: ").strip()

    # Step 1: Load and Chunk Document
    try:
        print("\n🔍 Processing document...")
        chunks = load_and_chunk_document(file_path)
        print(f"✅ Document split into {len(chunks)} chunks.")
    except Exception as e:
        print(f"❌ Error loading document: {e}")
        return

    # Step 2: Initialize Retriever & Generator
    retriever = DocumentRetriever()
    generator = ResponseGenerator()

    # Step 3: Index the document
    retriever.add_documents(chunks)

    # Step 4: Interactive QA Loop
    print("\n💬 You can now ask questions based on the document.")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nYou: ")
        if query.lower() in ['exit', 'quit']:
            print("👋 Exiting chatbot. Goodbye!")
            break

        relevant_chunks = retriever.retrieve(query)
        context_texts = [doc["text"] for doc in relevant_chunks]
        answer = generator.generate_response(query, context_texts)

        print("\n🤖 Answer:")
        print(answer)

if __name__ == "__main__":
    main()
