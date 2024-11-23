from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database configuration
DATABASE_URL = "sqlite:///./chats.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class ChatRecord(Base):
    __tablename__ = "chat_records"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_message = Column(Text,nullable=True)
    model_response = Column(Text,nullable=True)
    name = Column(String, nullable=True)  # New field for name
    email = Column(String, nullable=True)  # New field for email
    phone_number = Column(String, nullable=True)  # New field for phone number
    role=Column(String,nullable=True)
    transfer_call_user_message = Column(Text, nullable=True) 
    transfer_call_response = Column(Text, nullable=True) 



# Create all tables in the database
Base.metadata.create_all(bind=engine)
