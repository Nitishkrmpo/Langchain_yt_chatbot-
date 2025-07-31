import streamlit as st
import requests
import time
import uuid
import json
import os
from langchain.schema import Document  # Import Document class for serialization

# Configuration
BACKEND_URL = "http://localhost:5000"
CHAT_DATA_DIR = "chat_data"

# Create chat data directory if not exists
os.makedirs(CHAT_DATA_DIR, exist_ok=True)

# Initialize session state
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'collection_name' not in st.session_state:
    st.session_state.collection_name = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'video_url' not in st.session_state:
    st.session_state.video_url = ""
if 'language' not in st.session_state:
    st.session_state.language = "en"
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'chat_data' not in st.session_state:
    st.session_state.chat_data = {
        "video_url": "",
        "session_id": "",
        "language": "",
        "conversation": []
    }
if 'exiting' not in st.session_state:
    st.session_state.exiting = False

# Language mapping
LANGUAGE_MAP = {
    "English": "en", "Hindi": "hi", "Spanish": "es", "French": "fr", "German": "de",
    "Portuguese": "pt", "Italian": "it", "Dutch": "nl", "Japanese": "ja", "Korean": "ko",
    "Russian": "ru", "Chinese": "zh", "Arabic": "ar", "Turkish": "tr", "Vietnamese": "vi",
    "Indonesian": "id", "Thai": "th", "Swedish": "sv", "Polish": "pl", "Finnish": "fi", "Danish": "da"
}

# Function to serialize LangChain Document objects
def serialize_document(doc):
    """Convert LangChain Document to serializable dictionary"""
    if isinstance(doc, Document):
        return {
            "page_content": doc.page_content,
            "metadata": doc.metadata
        }
    # Handle other types if needed
    return doc

# Function to start session
def start_session():
    try:
        response = requests.post(f"{BACKEND_URL}/start_session")
        if response.status_code == 200:
            st.session_state.session_id = response.json().get("session_id")
            return True
        else:
            st.error(f"Failed to start session: {response.json().get('error', 'Unknown error')}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return False

# Function to process video
def process_video():
    """Send processing request to backend"""
    if not st.session_state.session_id:
        st.error("Session not started")
        st.session_state.processing = False
        return
        
    payload = {
        "url": st.session_state.video_url,
        "lang": LANGUAGE_MAP[st.session_state.language],
        "session_id": st.session_state.session_id
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/process_youtube", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.session_state.collection_name = result.get("collection")
            st.session_state.processing = False
            st.success("✅ Video processed successfully!")
            st.session_state.messages = [{"role": "assistant", "content": "Ask me anything about the video!"}]
            
            # Initialize chat data
            st.session_state.chat_data = {
                "video_url": st.session_state.video_url,
                "session_id": st.session_state.session_id,
                "language": st.session_state.language,
                "conversation": []
            }
        else:
            st.error(f"Error processing video: {response.json().get('error', 'Unknown error')}")
            st.session_state.processing = False
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        st.session_state.processing = False

# Function to ask question
def ask_question(query):
    """Send question to backend and return response with context"""
    if not st.session_state.collection_name:
        return "Error: No video has been processed yet", []
    if not st.session_state.session_id:
        return "Error: Session not started", []
    
    payload = {
        "query": query,
        "collection": st.session_state.collection_name,
        "session_id": st.session_state.session_id
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/ask", json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response received"), data.get("context", [])
        else:
            return f"Error: {response.json().get('error', 'Unknown error')}", []
    except requests.exceptions.RequestException as e:
        return f"Connection error: {str(e)}", []

# Function to save chat data to file
def save_chat_data():
    """Save chat conversation to JSON file"""
    if not st.session_state.chat_data["conversation"]:
        return None
    
    filename = f"{CHAT_DATA_DIR}/chat_{st.session_state.session_id}_{int(time.time())}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(st.session_state.chat_data, f, indent=2)
        return filename
    except Exception as e:
        st.error(f"Error saving chat: {str(e)}")
        return None

# Function to display context sources
def display_context(context):
    """Show context in a user-friendly format"""
    if not context:
        return
    
    with st.expander("📚 Sources Used (Click to Expand)", expanded=False):
        for i, doc in enumerate(context):
            # Handle both raw Document objects and serialized versions
            if isinstance(doc, Document):
                content = doc.page_content
                metadata = doc.metadata
            else:
                content = doc.get("page_content", "")
                metadata = doc.get("metadata", {})
            
            st.subheader(f"Source #{i+1}")
            st.caption(f"**Metadata:** {json.dumps(metadata, indent=2)}")
            st.markdown(f"**Content:**\n{content}")
            st.divider()

# Function to exit and save chat
def exit_and_save():
    """Save chat data and reset state"""
    filename = save_chat_data()
    
    # Reset session state
    st.session_state.processing = False
    st.session_state.collection_name = None
    st.session_state.messages = []
    st.session_state.session_id = None
    st.session_state.chat_data = {
        "video_url": "",
        "session_id": "",
        "language": "",
        "conversation": []
    }
    st.session_state.exiting = True
    
    return filename

# Main app layout
st.title("🎬 YouTube Video Chat Analyzer")

# Create two columns
input_col, chat_col = st.columns([1, 2])

# Left column - Input form
with input_col:
    st.header("1. Video Input")
    
    with st.form("video_form"):
        st.session_state.video_url = st.text_input(
            "🔗 YouTube URL", 
            placeholder="https://www.youtube.com/watch?v=...",
            value=st.session_state.video_url
        )
        
        st.session_state.language = st.selectbox(
            "🌐 Language", 
            options=list(LANGUAGE_MAP.keys()),
            index=0
        )
        
        process_btn = st.form_submit_button(
            "📄 Process Video", 
            disabled=st.session_state.processing,
            type="primary"
        )
    
    if process_btn:
        if not st.session_state.video_url:
            st.error("Please enter a YouTube URL")
        else:
            st.session_state.processing = True
            st.session_state.collection_name = None
            st.session_state.messages = []
            st.session_state.exiting = False
            
            # Start session before processing video
            if start_session():
                process_video()
            else:
                st.session_state.processing = False
    
    # Add Exit and Save button
    if st.session_state.chat_data.get("conversation") and not st.session_state.exiting:
        if st.button("🚪 Exit and Save Chat", type="primary", use_container_width=True):
            filename = exit_and_save()
            if filename:
                st.success(f"💾 Chat saved to {filename}")
                st.info("Chat session ended. To start a new session, process a video.")
                st.session_state.exiting = True

# Right column - Chat interface
with chat_col:
    st.header("2. Chat with Video Content")
    
    # Show processing status
    if st.session_state.processing:
        with st.status("Processing video...", expanded=True) as status:
            st.write("Starting session...")
            st.write("Downloading transcript...")
            st.write("Splitting content...")
            st.write("Creating embeddings...")
            time.sleep(1)  # Simulate processing time
    
    # Chat container
    chat_container = st.container()
    
    # Display chat messages
    with chat_container:
        for message in st.session_state.messages:
            role = "assistant" if message["role"] == "ai" else message["role"]
            with st.chat_message(role):
                st.markdown(message["content"])
    
    # User input handling
    if not st.session_state.exiting:
        if prompt := st.chat_input(
            "Ask something about the video...", 
            key="user_input",
            disabled=st.session_state.collection_name is None
        ):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message immediately
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Display assistant response
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    
                    # Get response from API with context
                    response, context = ask_question(prompt)
                    
                    # Serialize context for storage and display
                    serialized_context = [serialize_document(doc) for doc in context]
                    
                    # Add to chat data with full context
                    st.session_state.chat_data["conversation"].append({
                        "question": prompt,
                        "answer": response,
                        "context": serialized_context  # Store serialized context
                    })
                    
                    # Simulate streaming
                    if response.startswith("Error:"):
                        # Show error immediately
                        message_placeholder.error(response)
                    else:
                        for word in response.split():
                            full_response += word + " "
                            message_placeholder.markdown(full_response + "▌")
                            time.sleep(0.03)
                        message_placeholder.markdown(full_response)
                        
                    # Display context sources if available
                    if context:
                        display_context(serialized_context)
            
            # Add assistant response to messages
            st.session_state.messages.append({"role": "ai", "content": response})
    else:
        st.info("💬 Chat session has ended. Process a new video to start a new session.")