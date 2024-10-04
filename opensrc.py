from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

load_dotenv()

# Langsmith : Monitoring
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# prompt template

prompt = ChatPromptTemplate.from_messages(
    [
    
        ("user", "Question: {question}")
    ]
)



# streamlit

st.title("Chatbot with LLama")
input_text = st.text_input("Enter the topic: ")

#llm

llm = Ollama(model="llama3.2")
output_parser = StrOutputParser()
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))
