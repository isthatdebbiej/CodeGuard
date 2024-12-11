import streamlit as st
from owasp import OWASPCodeAnalyzer

class StreamlitApp:
    def __init__(self):
        self.analyzer = OWASPCodeAnalyzer()

    def run(self):
        st.title("Code Review Chat Assistant with RAG")
        st.write("Paste your code snippet below to analyze it for OWASP vulnerabilities.")
        code_snippet = st.text_area("Code Snippet", height=300)

        if st.button("Analyze Code"):
            if code_snippet.strip():
                st.subheader("OWASP Vulnerabilities Detected")
                llama_feedback = self.analyzer.generate_llama_analysis(code_snippet)
                st.info(llama_feedback)
            else:
                st.error("Please paste a code snippet for analysis.")

if __name__ == '__main__':
    app = StreamlitApp()
    app.run()
