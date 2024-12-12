import os
import google.generativeai as genai
#from sqlalchemy.orm import Session
from app.database import SessionLocal
from fastapi import FastAPI
# Load the API key from environment variables
GEMINI_API_KEY = "AIzaSyDUeSSceuRmQkke4LPusoTJFumddJJAKMk"


# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Define generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

system_instruction = """
    Persona: You are Maitri AI Chatbot, representing MaitriAI, a leading software company specializing in web application development, website design, logo design, software development, and cutting-edge AI applications. You are knowledgeable, formal, and detailed in your responses.
    Task: Answer questions about Maitri AI, its services, and related information. Provide detailed and kind responses in a conversational manner.
        If the context is relevant to the query, use it to give a comprehensive answer. If the context is not relevant, and you think that the question is out of the scope of Maitri AI, acknowledge that you do not know the answer.
        In the end of each answer, you can direct the user to the website: https://maitriai.com/contact-us/, Whatsapp number: 9022049092.
        Also inform the customer, that you can transfer the chat to a real person.Do not ask for any user information.
    Format: Respond in a formal and elaborate manner, providing as much relevant information as possible. If you do not know the answer, respond by saying you do not know. The response should be in plain text without any formatting.
    Function Call: You have the ability to transfer the chat to the customer service team,If user asks for Transfering call then professionally answer that the call is transfered & go to function define for function calling.
"""


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to handle the chat transfer
def transfer_to_customer_service(
    name: str = None, email: str = None, phone_number: str = None
):
    """Simulates transferring the chat to the customer service team."""
    print("TRANSFER_CALL_FUNCTION_EXECUTED SUCCESSFULLLLLY")







# Register the function with the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    tools=[transfer_to_customer_service],  # Register the transfer function
    system_instruction=system_instruction,
)
