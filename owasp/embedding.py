from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

class OWASPEmbedding:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.vector_store, self.texts = self.create_vector_store()

    def create_vector_store(self):
        index = faiss.IndexFlatL2(self.model.get_sentence_embedding_dimension())
        return index, []

    def generate_embeddings(self, texts):
        return np.array(self.model.encode(texts))

    def add_to_vector_store(self, texts):
        embeddings = self.generate_embeddings(texts)
        self.vector_store.add(embeddings)
        self.texts.extend(texts)

    def search_in_vector_store(self, query, top_k=5):
        if not self.vector_store.ntotal:
            return [], []  
        query_embedding = self.generate_embeddings([query])
        distances, indices = self.vector_store.search(query_embedding, top_k)
        results = [(self.texts[idx], dist) for idx, dist in zip(indices[0], distances[0]) if idx < len(self.texts)]
        return results
