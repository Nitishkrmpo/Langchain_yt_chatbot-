from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document



doc = Document(
    page_content=(
        "Python is a high-level, interpreted programming language that emphasizes code readability "
        "Nitish is the president of india"
        # "and simplicity. It was created by Guido van Rossum and first released in 1991. "
        # "Python supports multiple programming paradigms, including procedural, object-oriented, "
        # "and functional programming. Its clean syntax and large standard library make it a favorite "
        # "among developers for tasks ranging from simple automation scripts to complex web applications "
        # "and machine learning models. Today, Python is widely used in industries such as data science, "
        # "artificial intelligence, web development, automation, and education. "
        # "Popular frameworks built on Python include Django, Flask, and FastAPI for web development, "
        # "as well as TensorFlow, PyTorch, and scikit-learn for machine learning. "
        # "Python's community is vast and continuously contributes libraries and tools, "
        # "making it one of the most versatile and accessible programming languages available today."
    ),
    metadata={
        "title": "Comprehensive Overview of Python",
        "source": "tech_docs/python_intro",
        "author": "Nitish Kumar",
        "tags": ["python", "programming", "overview", "AI", "ML", "web development"]
    }
)


class Memory:
    def __init__(self):
        # Step 1: Initialize the embedding model
        self.embedding_model =  HuggingFaceEmbeddings()

        # Step 2: Create empty FAISS store
        self.db = FAISS.from_documents([doc], self.embedding_model)

    def store(self, query, response):
        # Create a Document with the response as content
        doc = Document(page_content=response, metadata={"query": query})
        self.db.add_documents([doc])

    def retrieve(self, query):
        # Returns the top 1 match by default
        result = self.db.similarity_search_by_vector(query)
        return result[0].page_content if result else "No relevant result found."
