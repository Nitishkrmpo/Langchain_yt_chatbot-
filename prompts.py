# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# prompts.py
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)

system_template = """You are an expert assistant for question-answering about YouTube videos. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Keep your answers concise and relevant to the video content.

Context: {context}

Previous conversation:
{chat_history}"""
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template = "{query}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

# Create the chat prompt with memory placeholder
chat_template= ChatPromptTemplate.from_messages([
    system_message_prompt,
    MessagesPlaceholder(variable_name="chat_history"),
    human_message_prompt
])
# chat_history = []
# # load chat history
# with open('chat_history.txt') as f:
#     chat_history.extend(f.readlines())

# print(chat_history)

# create prompt

