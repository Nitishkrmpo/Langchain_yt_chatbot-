from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from agent.memory import Memory
from agent.tools import search_tool
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_community.llms import HuggingFacePipeline
from langchain_huggingface.chat_models import ChatHuggingFace
from transformers import pipeline
class AgentController:
    def __init__(self):
        load_dotenv()
        self.llm = self._load_huggingface_model()
        self.memory = Memory()


    def _load_huggingface_model(self):
        """
        Initializes and returns a HuggingFacePipeline model instance (for local inference).
        """
        llm = ChatGroq(
        # model_name="gemma2-9b-it",  # Other options: "llama3-70b-8192", "gemma-7b-it"
        model_name="llama-3.3-70b-versatile",
        temperature=0.0,
        max_retries=2
        )
       
        return llm


    def process_request(self, user_query):
        """
        Handles a user's query:
        - Checks memory for a cached response.
        - If not found, uses search_tool and the LLM to generate a response.
        - Stores the result in memory before returning.
        """
        # past_data = self.memory.retrieve(user_query)
        # if past_data:
        #     return past_data
        print("call hua")
        search_results = search_tool(user_query)
        print(f"Search results: {search_results}")
        prompt = f"Based on this info: {search_results}, answer: {user_query}"
        print(f"Prompt: {prompt}")
        response = self.llm.invoke(prompt)

        self.memory.store(user_query, response.content)
        return response.content

