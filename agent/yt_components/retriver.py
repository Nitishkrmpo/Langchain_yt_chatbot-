import os , sys 
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

from .embedder import embedder
from langchain.retrievers.document_compressors import LLMChainExtractor
from agent_controller import AgentController
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever

# from langchain.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.schema import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Optional: AgentController from your codebase
from agent_controller import AgentController  # Adjust path


def build_compression_retriever(file_name: str, collection_name: str) -> ContextualCompressionRetriever:
    # Step 1: Load documents
    # documents = load_documents(file_name)

    # Step 2: Initialize LLM and Compressor
    llm = AgentController()._load_huggingface_model()
    compressor = LLMChainExtractor.from_llm(llm)

    
    vector_store=embedder(transcript_chunk_file=file_name,collection_name=collection_name)
    # Step 4: Setup retrievers
    base_retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    compression_retriever = ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=compressor
    )

    return compression_retriever

def build_compression_retriever_from_collection(collection_name):
    """Create compression retriever from existing ChromaDB collection"""
    from langchain.vectorstores import Chroma
    from agent.yt_components.embedder import embedding_model1
    
    # Create vector store from existing collection
    llm = AgentController()._load_huggingface_model()
    compressor = LLMChainExtractor.from_llm(llm)
    vector_store = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model1,
        collection_name=collection_name
    )
    
    # Create base retriever
    base_retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    # Create compression retriever
    return ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=compressor
    )