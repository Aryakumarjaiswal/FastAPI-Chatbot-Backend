from pydantic import BaseModel


class ChatRecordCreate(BaseModel):
    session_id: str
    user_message: str
    model_response: str
