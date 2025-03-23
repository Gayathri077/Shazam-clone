import os
import tempfile
import streamlit as st
import whisper
import subprocess
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- 🔹 Streamlit UI ---
st.set_page_config(page_title="Shazam Clone - Audio Subtitle Search", layout="centered")

# --- 🔹 Load API Key Securely ---
API_KEY_PATH = r"C:/Users/HP/Documents/api_key.txt"
if os.path.exists(API_KEY_PATH):
    with open(API_KEY_PATH, "r") as f:
        GOOGLE_API_KEY = f.read().strip()
else:
    st.error("❌ Google API Key file not found. Check the path.")
    st.stop()

# --- 🔹 Ensure FFmpeg is Installed ---
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
        return True
    except FileNotFoundError:
        return False

# --- 🔹 Initialize Embedding Model ---
@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

embedding_model = get_embedding_model()

# --- 🔹 Load and Process Subtitle Files ---
@st.cache_data
def load_documents():
    """Load subtitle files and split them into chunks for vector search."""
    subtitles_path = r"Downloads/Cleaned_Subtitles"
    
    if not os.path.exists(subtitles_path):
        os.makedirs(subtitles_path, exist_ok=True)
        st.error("❌ Subtitle folder not found. It has been created. Add subtitle files and rerun.")
        return []

    st.info("📂 Loading subtitle files...")
    loader = DirectoryLoader(subtitles_path, glob="*.txt", show_progress=True, loader_cls=TextLoader)
    docs = loader.load()

    if not docs:
        st.warning("⚠️ No subtitle files found in the directory.")
        return []

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(docs)

# --- 🔹 Initialize ChromaDB ---
@st.cache_resource
def get_database():
    """Create or load a ChromaDB vector database."""
    db_path = "./chroma_db/"
    os.makedirs(db_path, exist_ok=True)

    db = Chroma(collection_name="vector_database", embedding_function=embedding_model, persist_directory=db_path)

    if len(db.get()) == 0:
        chunks = load_documents()
        if chunks:
            db.add_documents(chunks)

    return db

db = get_database()

# --- 🔹 Transcribe Audio using Whisper ---
def transcribe_audio_whisper(audio_path):
    """Convert speech to text using OpenAI Whisper."""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        model = whisper.load_model("base")  # Use 'small', 'medium', or 'large' for better accuracy
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return f"Error during transcription: {str(e)}"

# --- 🔹 Generate Response using AI Model ---
def generate_response(query, context_text):
    """Generate AI-based response using Google Gemini API."""
    PROMPT_TEMPLATE = """
    You are an AI assistant providing **accurate, well-structured, and context-specific** responses.

    ### Context:
    {context}

    ### Question:
    {question}

    ### Guidelines:
    - Provide a **clear and structured** response.
    - Use **bullet points** for better readability.
    - Maintain **proper line spacing and word spacing**.
    - Stick **strictly to the provided context**; **do not assume or infer** beyond it.
    - If the context is insufficient, politely indicate that.

    ### Output:
    If a relevant subtitle is found, provide:
    1. The **subtitle text**.
    2. The **corresponding URL**.
    """


    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)

    chat_model = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY)
    parser = StrOutputParser()

    chain = prompt | chat_model | parser
    return chain.invoke({'context': context_text, 'question': query})

# --- 🔹 Streamlit UI ---
st.title("🎙️Shazam Clone - Audio to Subtitle Search")
st.markdown("Upload an **audio file**, and the app will find matching subtitles.")

# --- 🔹 File Uploader ---
uploaded_file = st.file_uploader("🎧 Upload an audio file (MP3/WAV/M4A)", type=["wav", "mp3", "m4a"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    st.audio(temp_audio_path, format=f"audio/wav")

    # --- 🎤 Transcribe Audio ---
    query = transcribe_audio_whisper(temp_audio_path)
    st.subheader("🎤 Transcribed Query")
    st.write(query)
    if not query:
        st.warning("⚠️ Could not transcribe the audio. Try again with a clearer file.")
    else:
        # --- 🔍 Search ChromaDB for Matching Subtitles ---
        docs_chroma = db.similarity_search_with_score(query, k=3)

        if docs_chroma:
            context_text = "\n\n".join([doc.page_content for doc, _ in docs_chroma])
            response = generate_response(query, context_text)
            st.write("### ✅ Best Matching Subtitle:", response) 