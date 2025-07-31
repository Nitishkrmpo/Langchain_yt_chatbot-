from agent.agent_controller import AgentController
from prompts import chat_template
from agent.yt_components.retriver import build_compression_retriever_from_collection
from langchain.chains import LLMChain

def main_chat_response(query: str, video_id: str) -> str:
    """
    Generate LLM response using LangChain message format
    """
    # Get retriever for this video
    retriever = build_compression_retriever_from_collection(f"yt_{video_id}")
    
    # Retrieve context
    context_docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in context_docs])
    
    # Create message chain
    llm = AgentController()._load_huggingface_model()
    messages = chat_template.format_messages(context=context, query=query)
    
    # Generate response
    response = llm(messages)
    return response.content