import os
import streamlit as st
from owasp import OWASPCodeAnalyzer

# Initialize OWASP Analyzer with the API Key
CEREBRAS_API_KEY = st.secrets.CEREBRAS_API_KEY
analyzer = OWASPCodeAnalyzer(api_key=CEREBRAS_API_KEY)

class StreamlitApp:
    def __init__(self):
        self.analyzer = analyzer

    def run(self):
        # Set page layout to wide mode
        st.set_page_config(layout="wide")

        # Custom CSS for styling
        st.markdown(
            """
            <style>
            /* Style for columns */
            .column-border {
                border: 1px solid #d3d3d3;
                border-radius: 5px;
                padding: 10px;
                background-color: white;
                height: 600px;
                overflow: auto;
            }
            textarea {
                background-color: #1e1e1e !important;
                color: white !important;
                border: none !important;
                font-family: "Courier New", Courier, monospace;
                font-size: 14px;
            }
            /* Style for the Analyze button */
            .stButton>button {
                background-color: #ff4d4f;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            /* Align Analyze button to the top-right */
            .top-right-button {
                position: absolute;
                top: 20px;
                right: 20px;
                z-index: 1000;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Title and description
        st.title("OWASP Code Analyzer")
        st.write("Paste your code snippet on the left and view the analysis on the right.")

    
        analyze_button = st.button("Analyze", key="analyze_top_right", help="Click to analyze code")


        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.subheader("Code Input")
            code_snippet = st.text_area(
                "",
                placeholder="Write or paste your code here...",
                key="code_input",
                height=500,
                label_visibility="collapsed",
            )

        with col2:
            st.subheader("Secure Code")
            if "analysis" in st.session_state:
                st.text_area(
                    "",
                    value=st.session_state["analysis"],
                    height=500,
                    label_visibility="collapsed",
                )
            else:
                st.text_area(
                    "",
                    value="Results will appear here after you analyze the code.",
                    height=500,
                    label_visibility="collapsed",
                )

        if analyze_button:
            if code_snippet:
                try:
                    with st.spinner("Analyzing code..."):
                        analysis = self.analyzer.generate_cerebras_analysis(code_snippet)
                    st.session_state["analysis"] = analysis.content
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a code snippet to analyze.")

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
