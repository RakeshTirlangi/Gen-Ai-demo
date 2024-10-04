from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable Langsmith Monitoring
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Change this to specific domains if needed, e.g. ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Initialize LLM and prompt templates
llm = Ollama(model="llama3.2")
output_parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages([("user", "Question: {question}")])

# Define a request model for the API
class QuestionRequest(BaseModel):
    question: str

# API endpoint to handle the chatbot interaction
@app.post("/ask")
async def ask_question(question_request: QuestionRequest):
    # Extract the input question
    input_question = question_request.question

    # Invoke the LLM chain
    try:
        result = prompt | llm | output_parser
        response = result.invoke({"question": input_question})
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}

# Run the API with Uvicorn (use `uvicorn app:app --reload` to run)
