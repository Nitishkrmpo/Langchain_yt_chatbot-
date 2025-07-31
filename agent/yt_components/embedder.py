
import torch
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain.schema import Document
import torch
import re
# from web import video_id
from typing import List
import os
# from retriver import compression_retriever
# E5 models need prefixing: "query: " or "passage: " for optimal performance
# You can use `encode_kwargs` to control pooling strategy
load_dotenv()
embedding_model1 = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        # "use_auth_token": "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"
    },
    encode_kwargs={"normalize_embeddings": True}  # important for similarity
)




def embedder(
    transcript_chunk_file: str,
    collection_name: str,
    persist_dir: str = "chroma_db",
    
    embedding_model: HuggingFaceEmbeddings = embedding_model1
) -> Chroma:
    """
    Embeds semantically split transcript chunks using HuggingFace embeddings and stores them in a Chroma DB.

    Parameters:
        transcript_chunk_file (str): Path to the file containing semantically split chunks.
        embedding_model (HuggingFaceEmbeddings): The embedding model to be used.
        persist_dir (str): Directory to persist Chroma vector DB.
        collection_name (str): Name of the vector store collection.

    Returns:
        Chroma: A Chroma vector store instance containing embedded documents.
    """

    if not os.path.exists(transcript_chunk_file):
        raise FileNotFoundError(f"❌ File not found: {transcript_chunk_file}")

    # ✅ Load chunks from file
    with open(transcript_chunk_file, "r", encoding="utf-8") as f:
        content = f.read()

    raw_chunks = re.split(r"chunk \d+\s*:", content)
    chunks = [chunk.strip() for chunk in raw_chunks if chunk.strip()]

    # ✅ Wrap each chunk as a Document
    docs: List[Document] = [
        Document(page_content=chunk, metadata={"source": f"chunk{i}"})
        for i, chunk in enumerate(chunks)
    ]

    print(f"📦 Total documents to embed: {len(docs)}")

    # ✅ Create and populate the vector store
    vector_store = Chroma(
        embedding_function=embedding_model1,
        persist_directory=persist_dir,
        collection_name=collection_name
    )
    vector_store.add_documents(docs)

    print(f"✅ Documents embedded and stored in '{persist_dir}' (collection: '{collection_name}')")

    return vector_store


