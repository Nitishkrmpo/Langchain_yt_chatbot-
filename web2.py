from flask import Flask, request, jsonify
from agent.yt_components.transcripts import download_youtube_auto_subtitles, parse_vtt_to_text
from agent.yt_components.splitter import semantic_splitter
from agent.yt_components.retriver import build_compression_retriever, build_compression_retriever_from_collection
from agent.agent_controller import AgentController
from prompts import chat_template
import os
import uuid
from pathlib import Path
from langchain.memory import ConversationBufferMemory

app = Flask(__name__)

# Create directories if they don't exist
Path("vtt_files").mkdir(exist_ok=True)
Path("transcripts").mkdir(exist_ok=True)
Path("chunked_files").mkdir(exist_ok=True)

# Global dictionary to store conversation memories
conversation_memories = {}

@app.route("/start_session", methods=["POST"])
def start_session():
    """Initialize a new conversation session"""
    session_id = str(uuid.uuid4())
    conversation_memories[session_id] = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    return jsonify({"session_id": session_id})

@app.route("/process_youtube", methods=["POST"])
def process_youtube():
    data = request.json
    url = data.get("url")
    lang = data.get("lang", "en")
    session_id = data.get("session_id")  # Get session_id from client

    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400

    try:
        print(f"🔗 Processing URL: {url} for session {session_id}")

        # Download and parse subtitles
        vtt_file = download_youtube_auto_subtitles(url, lang, output_dir="vtt_files")
        
        # Parse VTT to text
        transcript = parse_vtt_to_text(vtt_file)
        transcript_txt = f"transcripts/clean_transcript_{session_id}.txt"
        with open(transcript_txt, "w", encoding="utf-8") as f:
            f.write(transcript)

        # Semantic chunking
        chunk_file = f"chunked_files/splitted_{session_id}.txt"
        semantic_splitter(transcript_txt, chunk_file)

        # Embed and build retriever
        collection_name = f"yt_{session_id}"
        build_compression_retriever(
            chunk_file, 
            collection_name=collection_name
        )

        # Ensure memory exists for this session
        if session_id not in conversation_memories:
            conversation_memories[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )

        return jsonify({
            "message": "✅ Transcript processed and retriever built", 
            "collection": collection_name,
            "session_id": session_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query")
    collection_name = data.get("collection")
    session_id = data.get("session_id")

    if not query or not collection_name or not session_id:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        # Get memory for this session
        memory = conversation_memories.get(session_id)
        if not memory:
            return jsonify({"error": "Invalid session ID"}), 400

        # Build retriever
        retriever = build_compression_retriever_from_collection(collection_name)
        
        # Retrieve context
        context_docs = retriever.get_relevant_documents(query)
        context = "\n\n".join([doc.page_content for doc in context_docs])
        
        # Create the chat prompt
        chat_history = memory.load_memory_variables({})["chat_history"]
        messages = chat_template.format_messages(
            context=context,
            chat_history=chat_history,
            query=query
        )
        
        # Generate response
        llm = AgentController()._load_huggingface_model()
        response = llm(messages)
        
        # Save context to memory
        memory.save_context({"input": query}, {"output": response.content})
        
        return jsonify({
            "response": response.content,
            "session_id": session_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)