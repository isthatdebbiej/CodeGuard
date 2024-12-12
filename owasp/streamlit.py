import os
import streamlit as st
from owasp import OWASPCodeAnalyzer

# Sidebar to input API Key
# with st.sidebar:
#     st.title("Settings")
#     st.markdown("### :red[Enter your Cerebras API Key below]")
#     CEREBRAS_API_KEY = st.text_input("Cerebras API Key:", type="password")

# # Display welcome message and stop if no API key is provided
# if not CEREBRAS_API_KEY:
#     st.markdown(
#         """
#         ## Welcome to the OWASP Code Analysis Demo!

#         This tool analyzes your code snippets and provides feedback based on OWASP error handling guidelines using Cerebras.

#         To get started:
#         1. :red[Enter your Cerebras API Key in the sidebar.]
#         2. Paste a code snippet below for analysis.
#         3. Click "Analyze" to get feedback on your code.
#         """
#     )
#     st.stop()

# Initialize OWASP Analyzer with the API Key
CEREBRAS_API_KEY = "csk-nxrtnpm9f35vnd94me9ke49mhm5jyh92w3epkhje6ejpxte6"
analyzer = OWASPCodeAnalyzer(api_key=CEREBRAS_API_KEY)

class StreamlitApp:
    def __init__(self):
        self.analyzer = analyzer

    def run(self):
        # Main title and description
        st.title("OWASP Code Analyzer with ChatCerebras")
        st.write("Upload your code snippet to get feedback based on OWASP error handling guidelines.")

        # Custom style for the text area
        st.markdown(
            """
            <style>
            textarea {
                width: 100% !important;
                min-height: 300px !important;
                max-height: 90vh !important;
                resize: vertical !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Code input area
        code_snippet = st.text_area(
            "Enter Code Snippet",
            placeholder="Paste your code here...",
            key="dynamic_textarea"
        )

        # Analysis button
        
        if st.button("Analyze"):
            if code_snippet:
                try:
                    # Perform the analysis
                    analysis = self.analyzer.generate_cerebras_analysis(code_snippet)
                    st.write(analysis)
                    # Check if the analysis contains errors
                    if analysis and 'content' in analysis:
                        errors = analysis.get('content', [])
                        if errors:
                            st.write("**Relevant Errors Found:**")
                            for error in errors:
                                st.subheader(f"{error['title']}")
                                st.write(f"**Description:** {error['description']}")
                                if 'suggestions' in error:
                                    st.write("**Suggestions:**")
                                    for suggestion in error['suggestions']:
                                        st.write(f"- {suggestion}")
            #             else:
            #                 st.write("No relevant errors found in the provided code snippet.")
            #         else:
            #             st.write("Unable to analyze the provided code snippet. Please check the input or try again later.")
                except Exception as e:
                    # Handle any exceptions that occur during the analysis process
                    st.error(f"An error occurred while analyzing the code snippet: {str(e)}")
            else:
                st.warning("Please enter a code snippet to analyze.")


if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
