# generator.py

import ollama

class ResponseGenerator:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name

    def generate_response(self, query: str, contexts: list) -> str:
        """
        Generate a structured response based on the query and retrieved contexts.
        """
        context_str = "\n\n".join(contexts)
        prompt = f"""
You are a helpful assistant. Answer the question strictly using only the context below.

CONTEXT:
{context_str}

QUESTION:
{query}

STRUCTURED ANSWER:
- Provide bullet points, tables, or well-formatted text if necessary.
- Keep it concise and relevant to the context.
"""

        response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()