from transformers import AutoModelForCausalLM, AutoTokenizer
from embedding import OWASPEmbedding

class OWASPCodeAnalyzer:
    def __init__(self, model_name="meta-llama"):
        self.model_name = model_name
        self.model, self.tokenizer = self.load_model()
        self.vector_store = OWASPEmbedding().vector_store

    def load_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForCausalLM.from_pretrained(self.model_name)
        return model, tokenizer

    def generate_llama_analysis(self, code_snippet):
        relevant_content = self.get_relevant_owasp_content(code_snippet)
        prompt = f"""
        Analyze the following code snippet based on the OWASP error handling guidelines:
        {relevant_content}
        Code snippet:
        {code_snippet}
        Provide detailed feedback and suggestions for improvement.
        """
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.model.generate(**inputs, max_length=1024, num_beams=5, early_stopping=True)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    def get_relevant_owasp_content(self, code_snippet):
        query = f"Analyze this code for OWASP vulnerabilities related to error handling: {code_snippet}"
        search_results = self.vector_store.similarity_search(query, k=2)
        return " ".join([result['text'] for result in search_results])
