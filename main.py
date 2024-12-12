from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.api import chat

app = FastAPI()
app.include_router(chat.router)

@app.get("/")
async def root1():
    """Function for Unregistered User"""
    return {"message": "Welcome to the Gemini Chat API!"}

