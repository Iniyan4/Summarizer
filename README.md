# 🎥 YouTube Transcript Summarizer

A Streamlit web app that:
- Extracts transcripts from YouTube videos using youtube-transcript-api
- Cleans and chunks long transcripts
- Summarizes using Hugging Face LLMs (e.g., Mistral-7B via Inference API)
- Translates summaries (optional)
- Exports results as .txt and .pdf
- Deployed on Streamlit Cloud



## 🚀 Demo

Try it live on *[[Streamlit Cloud](https://share.streamlit.io/YOUR_USERNAME/YOUR_REPO_NAME/main/app.py)](https://summarizer-haat5hfkctfunj5w26f88y.streamlit.app/)*



## Features

- ✅ YouTube transcript retrieval (multi-language supported)
- ✅ Chunking for LLM context size handling
- ✅ Hugging Face LLM summarization via InferenceClient
- ✅ Translation support (optional)
- ✅ Clean UI with Streamlit
- ✅ PDF and TXT download support
- ✅ Secrets managed securely with Streamlit Cloud



## Setup Instructions

```bash
1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

2. Create and Activate Virtual Environment

python -m venv venv
source venv/bin/activate        # On Windows: .\venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Add Hugging Face Token (Local Testing)

Create a .streamlit/secrets.toml file:

HF_TOKEN = "your-huggingface-api-key"

Ensure this file is in .gitignore:

.streamlit/secrets.toml


🧪 Run the App Locally

streamlit run app.py


☁ Deployment (Streamlit Cloud)

1. Push your code to GitHub


2. Go to Streamlit Cloud


3. Connect your GitHub repo


4. Add secrets under the "Secrets" tab:


5. Click "Deploy"



📂 Export Options

Summarized results can be:

Downloaded as .txt files

Exported to .pdf

Displayed cleanly as Scrollable Field in the UI



📦 Dependencies

streamlit

huggingface_hub

youtube-transcript-api

fpdf (for PDF export)

requests


🙌 Acknowledgements

Hugging Face

youtube-transcript-api

Streamlit

🙋‍♀️ Author

R.Iniyapadmanaban

CS24B1109

Powered by  Mistral, Streamlit, Hugging Face, and YouTube Transcript API



