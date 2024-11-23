from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.api import chat

app = FastAPI()
app.include_router(chat.router)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root1():
    """Function for Unregistered User"""
    return {"message": "Welcome to the Gemini Chat API!"}

