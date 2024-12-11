import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
from embedding import OWASPEmbedding

class OWASPCodeAnalyzer:
    def __init__(self, model_name="meta-llama/Meta-Llama-3-8B"):
        self.model_name = model_name
        self.token = self.read_token_from_file()
        self.model, self.tokenizer = self.load_model()
        self.vector_store = OWASPEmbedding().vector_store

    def read_token_from_file(self):
        """
        Reads Hugging Face token from a file located in the current directory.
        """
        try:
            token_file_path = os.path.join(os.path.dirname(__file__), 'token.txt')
            with open(token_file_path, 'r') as file:
                token = file.read().strip()
                return token
        except FileNotFoundError:
            raise FileNotFoundError("Token file 'token.txt' not found in the 'owasp' folder.")
        except Exception as e:
            raise Exception(f"Error reading token from file: {e}")

    def load_model(self):
        """
        Loads the model and tokenizer using the Hugging Face token.
        """
        if self.token:
            login(token=self.token)
        
        # Load the tokenizer and model with the authentication token
        tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_auth_token=self.token)
        model = AutoModelForCausalLM.from_pretrained(self.model_name, use_auth_token=self.token)
        return model, tokenizer

    def generate_llama_analysis(self, code_snippet):
        """
        Generates feedback on a code snippet based on OWASP error handling guidelines.
        """
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
        """
        Retrieves relevant OWASP content for a given code snippet based on error handling vulnerabilities.
        """
        query = f"Analyze this code for OWASP vulnerabilities related to error handling: {code_snippet}"
        search_results = self.vector_store.similarity_search(query, k=2)
        return " ".join([result['text'] for result in search_results])
