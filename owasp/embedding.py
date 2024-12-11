from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from scraper import CheatSheetScraper

class OWASPEmbedding:
    def __init__(self):
        self.vector_store = self.create_vector_store()

    def get_owasp_content(self):
        scraper = CheatSheetScraper()
        cheat_sheets = scraper.scrape_cheat_sheets()
        content_list = [content for content in cheat_sheets.values()]
        return content_list
    
    def create_vector_store(self):
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(self.get_owasp_content(), embeddings)
        return vector_store

    def get_relevant_owasp_content(self, code_snippet):
        query = f"Analyze this code for OWASP vulnerabilities related to error handling: {code_snippet}"
        search_results = self.vector_store.similarity_search(query, k=2)
        return " ".join([result['text'] for result in search_results])
