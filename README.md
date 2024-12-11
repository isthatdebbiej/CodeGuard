# CodeGuard: OWASP Vulnerability Detection Chat App

CodeGuard is a web-based app for detecting OWASP vulnerabilities related to error handling in code snippets. It leverages Streamlit for the UI, LLaMA for model-based analysis, and FAISS for efficient content search.

## Prerequisites

- Python 3.8+
- Git
- `pip` or `conda`

### Install Dependencies

1. Clone the repo:
   ```bash
   git clone https://github.com/isthatdebbiej/CodeGuard.git
   cd CodeGuard
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open the app in your browser at `http://localhost:8501`.

## How It Works

- **User Input**: Paste code into the Streamlit interface.
- **OWASP Content**: Relevant OWASP error-handling guidelines are fetched using FAISS.
- **LLaMA Analysis**: The LLaMA model analyzes the code and provides feedback.
- **Display**: Results are shown in the UI.

## File Structure

- `app.py`: Streamlit UI and backend logic.
- `scraper.py`: Scrapes OWASP cheat sheets.
- `embedding.py`: Manages FAISS vector store.
- `llama_analysis.py`: Interacts with LLaMA for analysis.
- `requirements.txt`: Python dependencies.

## License

MIT License – see the [LICENSE](LICENSE) file for details.
