# 🎙️ Shazam Clone – AI-Powered Audio-to-Subtitle Search

An AI-powered audio search application built with Python and Streamlit that converts spoken audio into text, searches subtitle content using semantic similarity, and generates context-based responses using Google Gemini.

## 📌 Project Overview

The Shazam Clone accepts an audio file, transcribes the spoken content using OpenAI Whisper, and searches a collection of subtitle files for semantically similar content.

Instead of relying only on exact keyword matching, the application uses Hugging Face sentence embeddings and ChromaDB vector search to retrieve relevant subtitle content.

The retrieved context is then passed to Google Gemini through LangChain to generate a context-based response.

### Core Workflow

Audio File
↓
OpenAI Whisper
↓
Speech-to-Text
↓
Semantic Vector Search
↓
ChromaDB
↓
Relevant Subtitle Context
↓
Google Gemini
↓
Context-Based Response

## ✨ Features

- 🎧 Upload audio files in WAV, MP3, or M4A format
- 🎤 Convert speech to text using OpenAI Whisper
- 📄 Load and process subtitle text files
- ✂️ Split subtitle content into smaller searchable chunks
- 🧠 Generate semantic embeddings using Hugging Face
- 🔍 Search subtitle content using ChromaDB vector similarity
- 🤖 Generate context-based responses using Google Gemini
- 🔗 Use LangChain for retrieval and Generative AI workflow
- 🖥️ Interactive Streamlit interface
- ⚡ Cache models and application resources for improved performance

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core application development |
| Streamlit | Web application interface |
| OpenAI Whisper | Audio transcription |
| LangChain | LLM and retrieval workflow |
| Google Gemini | Generative AI responses |
| Hugging Face | Sentence embeddings |
| ChromaDB | Vector database and semantic search |
| FFmpeg | Audio processing |

## 🔎 How It Works

### 1. Audio Upload

The user uploads an audio file through the Streamlit interface.

Supported formats:

- WAV
- MP3
- M4A

### 2. Speech-to-Text

The uploaded audio is processed using the OpenAI Whisper base model.

The application converts the spoken audio into a text query.

### 3. Subtitle Processing

Subtitle text files are loaded and divided into smaller chunks using a text splitter.

The application uses:

- Chunk size: 500
- Chunk overlap: 50

### 4. Embedding Generation

The subtitle chunks are converted into vector representations using the Hugging Face model:

sentence-transformers/all-mpnet-base-v2

### 5. Vector Search

The embeddings are stored in ChromaDB.

When a transcribed query is generated, the application performs similarity search and retrieves the most relevant subtitle results.

### 6. Generative AI Response

The retrieved subtitle context is passed to Google Gemini through LangChain.

The model generates a response based on the retrieved context.

## 📂 Project Structure

Shazam-clone/
│
├── app.py
├── chroma_db/
├── .gitignore
└── README.md

### app.py

Contains the main Streamlit application, including:

- Audio upload
- Whisper transcription
- Subtitle loading
- Text chunking
- Hugging Face embeddings
- ChromaDB vector search
- Gemini response generation
- Streamlit UI

### chroma_db/

Stores the local ChromaDB vector database used for semantic subtitle search.

## ⚙️ Requirements

Make sure the following are installed:

- Python 3.9+
- FFmpeg
- Google Gemini API key

Python dependencies include:

- streamlit
- openai-whisper
- langchain
- langchain-community
- langchain-google-genai
- langchain-huggingface
- langchain-chroma
- chromadb
- sentence-transformers

## 🚀 Installation

### 1. Clone the repository

git clone https://github.com/Gayathri077/Shazam-clone.git

cd Shazam-clone

### 2. Create a virtual environment

python -m venv venv

### Windows

venv\Scripts\activate

### macOS / Linux

source venv/bin/activate

### 3. Install dependencies

pip install streamlit openai-whisper langchain langchain-community langchain-google-genai langchain-huggingface langchain-chroma chromadb sentence-transformers

### 4. Install FFmpeg

FFmpeg must be installed and available in your system PATH.

Verify the installation:

ffmpeg -version

## 🔐 API Key Configuration

The application requires a Google Gemini API key.

For security, do not commit your API key to GitHub.

Use an environment variable or Streamlit secrets.

Example:

GOOGLE_API_KEY=your_api_key_here

Never upload API keys, passwords, or other secrets to a public repository.

## 📁 Subtitle Files

Place subtitle .txt files inside:

Downloads/Cleaned_Subtitles/

Example:

Downloads/
└── Cleaned_Subtitles/
    ├── subtitle_01.txt
    ├── subtitle_02.txt
    └── subtitle_03.txt

The application loads these files and creates searchable text chunks for semantic retrieval.

## ▶️ Run the Application

Start the Streamlit application with:

streamlit run app.py

Then open the local Streamlit URL shown in the terminal.

## 🧪 Example Workflow

1. Start the Streamlit application.
2. Upload an audio file.
3. The application transcribes the audio using Whisper.
4. The generated text is used as a search query.
5. ChromaDB retrieves the most similar subtitle chunks.
6. The retrieved context is sent to Gemini.
7. The application displays the generated response.

## 🎯 Key Concepts Demonstrated

- Speech-to-text processing
- Natural Language Processing
- Semantic search
- Vector databases
- Text embeddings
- Retrieval-Augmented Generation concepts
- Generative AI
- LLM integration
- Streamlit application development
- Python-based AI application development

## 🚧 Future Improvements

- Support for larger audio files
- Improved audio preprocessing
- Multiple Whisper model options
- Automatic subtitle file discovery
- Movie or media metadata integration
- Timestamp-based subtitle retrieval
- Cloud-based vector database
- Deployment as a public web application
- Secure environment-based API configuration

## 👩‍💻 Author

Gayathri T

GitHub:
https://github.com/Gayathri077

Project Repository:
https://github.com/Gayathri077/Shazam-clone
