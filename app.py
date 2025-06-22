import re
from io import BytesIO

import requests
import streamlit as st
from fpdf import FPDF
from huggingface_hub import InferenceClient
from youtube_transcript_api import YouTubeTranscriptApi

client = InferenceClient(provider="novita",
                         api_key=st.secrets["TOKEN"])

Languages = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Telugu": "te",
    "German": "de"
}

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match is not None else None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript])
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

def chunk_text(text, max_chars=5000):
    chunks = []
    while len(text) > max_chars:
        split = text[:max_chars].rfind('.')+1
        if split == 0:
            split = max_chars
        chunks.append(text[:split].strip())
        text = text[split:].strip()
    if text:
        chunks.append(text)
    return chunks

def summarize(chunk):
    messages = [
        {
            "role" : "user",
            "content":         f"<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n"
                               f"<|im_start|>user\nSummarize the following text:\n\n"
                               f"\n"
                               f"<|im_end|>\n"
                               f"<|im_start|>assistant \n\n{chunk}"
        }
    ]
    response = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=messages
    )
    return response.choices[0].message.content

def translate_text(text, target_language):
    if target_language == "en":
        return text
    response = requests.post("https://translate.argosopentech.com/translate_text", json={
        "q":text,
        "source": "en",
        "target": target_language,
        "format": "text"
    })
    return response.json().get("translatedText", text)

def export_to_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

def export_to_text(text):
    return BytesIO(text.encode("utf-8"))

st.set_page_config(page_title="Summarizer", layout="centered")
st.title("Summarizer and Translator")

video_url = st.text_input("Paste a Youtube Video URL : ")
target_language = st.selectbox("Translate Summary to : ", list(Languages.keys()))

if st.button("Summarize"):
    with st.spinner("Fetching transcripts and generating summary....."):
        video_id = extract_video_id(video_url)
        if video_id is None:
            st.error("Video URL is invalid")
        else:
            transcript = get_transcript(video_id)
            if transcript is None:
                st.error("Unable to fetch transcript")
            else:
                chunks = chunk_text(transcript)
                summaries = [summarize(c) for c in chunks]
                full_summary = "\n\n".join(summaries)
                translated = translate_text(full_summary, Languages[target_language])

                st.subheader("Full Transcript")
                st.text_area("Transcript", transcript, height=500)

                st.subheader("SUMMARY OUTPUT")
                st.text_area("Summary", translated, height=500)

                st.download_button("Download as PDF ", data=export_to_text(translated), file_name="summary.pdf")
                st.download_button("Download as Text ", data=export_to_text(full_summary), file_name="summary.txt")