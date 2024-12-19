import os
from embedding import OWASPEmbedding
from langchain_cerebras import ChatCerebras

class OWASPCodeAnalyzer:
    def __init__(self, api_key=None, model_name="llama3.1-8b"):
        self.model_name = model_name
        self.cerebras_api = ChatCerebras(api_key=api_key, model=model_name)
        embedding_model = OWASPEmbedding()
        self.vector_store = embedding_model.vector_store
        self.texts = embedding_model.texts

    def generate_cerebras_analysis(self, code_snippet):
        relevant_content = self.get_relevant_owasp_content(code_snippet)
        prompt = (
        f"Analyze the following code snippet based on the OWASP error handling guidelines:\n"
        f"{relevant_content}\nCode snippet:\n{code_snippet}\n"
        "Identify vulnerabilities and provide only the corrected and improved code as the output without any explanations, comments, or additional text. "
        "Ensure the output is in the same programming language as the provided snippet."
    )
        return self.cerebras_api.invoke(prompt)

    def get_relevant_owasp_content(self, code_snippet):
        if self.vector_store.ntotal == 0:
            return "No relevant OWASP content available."

        query = f"Analyze this code for OWASP vulnerabilities related to error handling: {code_snippet}"
        distances, indices = self.vector_store.search(self.vector_store.generate_embeddings([query]), top_k=2)
        relevant_content = [self.texts[idx] for idx in indices[0] if idx < len(self.texts)]
        return " ".join(relevant_content)
