import streamlit as st
from owasp import OWASPCodeAnalyzer

class StreamlitApp:
    def __init__(self):
        self.analyzer = OWASPCodeAnalyzer()

    def run(self):
        st.title("OWASP Code Analyzer")
        st.write("Upload your code snippet to get feedback based on OWASP error handling guidelines.")

        code_snippet = st.text_area("Enter Code Snippet")
        
        if st.button("Analyze"):
            if code_snippet:
                analysis = self.analyzer.generate_llama_analysis(code_snippet)
                st.write("**Analysis Result:**")
                st.write(analysis)
            else:
                st.warning("Please enter a code snippet to analyze.")

# Instantiate and run the Streamlit app
app = StreamlitApp()
app.run()
