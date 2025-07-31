# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()
# import pandas as pd

# ✅ Create the semantic text splitter

from langchain_experimental.text_splitter import SemanticChunker
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from dotenv import load_dotenv
# import os
# load_dotenv()
from .embedder import embedding_model1 


def semantic_splitter(transcript_file_path: str, output_file_path: str, embedding_model=embedding_model1) -> list:
    """
    Splits a transcript into semantically meaningful chunks using LangChain's SemanticChunker.
    
    Parameters:
        transcript_file_path (str): Path to the cleaned transcript file.
        output_file_path (str): Path where the chunked transcript will be saved.
        embedding_model: An embedding model instance.
    
    Returns:
        List[Document]: A list of LangChain Document objects, each representing a chunk.
    """

    # ✅ Initialize SemanticChunker
    text_splitter = SemanticChunker(
        embedding_model,
        breakpoint_threshold_type="standard_deviation",
        breakpoint_threshold_amount= 0.5,
    )

    # ✅ Load the cleaned transcript
    with open(transcript_file_path, "r", encoding="utf-8") as f:
        scripts = f.read()
    
    print(f"📄 Input transcript length: {len(scripts)} characters")

    # ✅ Perform semantic chunking
    docs = text_splitter.create_documents([scripts])
    print(f"✅ Total chunks created: {len(docs)}")

    # ✅ Preview chunks
    for i, doc in enumerate(docs):
        print(f"🔹 Chunk {i+1}:\n{doc.page_content[:200]}...\n")

    # ✅ Export to output file
    with open(output_file_path, "w", encoding="utf-8") as f:
        for i, doc in enumerate(docs):
            f.write(f"chunk {i} : {doc.page_content.strip()}\n\n")
    
    print(f"✅ Exported all chunks to '{output_file_path}'")

    return docs
