# 🎬 RAG YouTube Video Chatting App

An AI-powered multilingual chatbot built with Retrieval-Augmented Generation (RAG) that answers questions based on YouTube video transcripts. The system uses **Gemma 2** for generation and **`intfloat/multilingual-e5-large`** for semantic embeddings, enabling accurate and context-rich responses in multiple languages.

---

## 🚀 Features

- 🌍 **Multilingual Embeddings**: Supports multiple languages with `intfloat/multilingual-e5-large`
- 🎬 **YouTube Transcript Analysis**: Interact with YouTube video content through natural conversation
- 🧠 **Gemma 2 LLM**: Lightweight open-source language model for fast, high-quality responses
- 🔍 **Semantic Search**: Retrieves relevant transcript segments using vector similarity
- ⚡ **RAG Pipeline**: Combines retrieval and generation for deep contextual understanding
- 💾 **ChromaDB Vector Store**: Efficient similarity search using in-memory or persisted vectors

---

## 📁 Project Structure

rag-youtube-chat-app/
├── yt_components/
│ ├── retriver.py # Document retriever using ChromaDB
│ ├── embedder.py # Loads and applies E5 embedding model
│ ├── query.py # Core RAG logic: retrieval + generation
├── transcripts/ # Saved YouTube transcripts
├── main.py # Main application runner
├── requirements.txt # Python dependencies
└── README.md # This documentation


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rag-youtube-chat-app.git
cd rag-youtube-chat-app


2. Create and Activate Environment
bash
Copy
Edit
conda create -n rag-env python=3.10 -y
conda activate rag-env
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory:

env
Copy
Edit
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
🔍 How It Works
Transcript Loading: Load local or fetched YouTube transcripts.

Embedding: Use intfloat/multilingual-e5-large to convert transcripts into semantic vectors.

Vector Store: Store these vectors in ChromaDB for similarity search.

Retrieval: Retrieve the most relevant transcript chunks using vector similarity.

Generation: Feed the retrieved context and user query to Gemma 2 to generate a natural response.

💬 Example Usage
python
Copy
Edit
# main.py

query = "What did the speaker say about transformers?"
response = chain.invoke({
    "query": query,
    "context": context
})
print(response)
✅ To-Do
 Auto-download YouTube transcripts via youtube_transcript_api

 Build a Streamlit or Gradio frontend for UI

 Support for multi-video document collections

 Dockerize for scalable deployment

 GPU acceleration for local Gemma 2 inference

🧠 Models Used
Component	Model Name	Source
Language Model	Gemma 2B or Gemma 2B IT	Gemma on Hugging Face
Embeddings	intfloat/multilingual-e5-large	E5 Model
Vector Store	ChromaDB	Chroma

📚 Dependencies
langchain

chromadb

transformers

sentence-transformers

torch

youtube-transcript-api

python-dotenv

👨‍💻 Author
Nitish Kumar
Built using open models and community-driven tools to make AI video understanding more accessible.

📜 License
This project is licensed under the MIT License.
See the LICENSE file for details.

yaml
Copy
Edit

---


