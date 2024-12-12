# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.config import model
# from app.database import SessionLocal
# from app.models.session_manager import SessionManager
# from app.database import ChatRecord
# from app.rag.rag_using_json1 import rag_using_json
# router2 = APIRouter()
# session_manager = SessionManager(model=model)


# # Dependency to get a database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @router.post("/chat(Guest)")
# async def chat(session_id: str, message: str,role:str, name: str = None, email: str = None, phone_number: str = None, db: Session = Depends(get_db)):
#     try:
#         # Validate user details and start conversation
#         user = db.query(Guest_ChatRecord).filter_by(name=name, email=email, phone_number=phone_number).first()
#         if user:
#             user.session_id=(session_id)
#             response_text = session_manager.send_message(session_id, message, name, email, phone_number)
#             user.user_message = (
#                 (user.user_message or "") + f"\n USER-> {message}"
#             )
#             user.model_response = (
#                (user.model_response or "") + f"\n RESPONSE-> {response_text}"
#             )
#             print(user.user_message)
#             db.commit()
#             db.refresh(user)
#         return {"session_id": session_id, "response": response_text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

# @router.post("/Not Registered")
# async def unregistered_user(name: str, email: str, mob_no: str, db: Session = Depends(get_db)):
#     """Function for Unregistered User"""
#     try:
#         user = db.query(ChatRecord).filter_by(email=email).first()

#         if user:
#             return {"message": f"User {name} already exists with email {email}!"}
        
#         else:

#         # Add new user to database
#             new_user = ChatRecord(name=name, email=email, phone_number=mob_no,role="Registered")
#             db.add(new_user)
#             db.commit()
#             db.refresh(new_user)

#             return {"message": f"User {name} has been added to the database!"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {e}")



# @router.post('/ChatTeam')
# async def chat_team(
#     session_id: str,
#     message: str,
#     role: str,
#     name: str = None,
#     email: str = None,
#     phone_number: str = None,
#     db: Session = Depends(get_db)
# ):
#     """Function for Chat Support Team"""
#     try:
#         # Validate user details
#         user = db.query(ChatRecord).filter_by(name=name, email=email, phone_number=phone_number).first()

#         if user:
#             # User exists in the database
#             # Append the chat session details to transfer_call columns
#             user.transfer_call_user_message = (
#                 (user.transfer_call_user_message or "") + f"\n USER-> {message}"
#             )
            
#             # Generate model response
#             chat_session = session_manager.get_chat_session(session_id)
#             prompt = rag_using_json(message=message)
#             response = chat_session.send_message(prompt)
#             response_text = "\n\n\n".join(
#                 part.text for part in response.candidates[0].content.parts if hasattr(part, "text")
#             )
#             print(response_text)

#             user.transfer_call_response = (
#                (user.transfer_call_response or "") + f"\n RESPONSE-> {response_text}"
#             )
#             print(user.transfer_call_response)
#             db.commit()
#             db.refresh(user)

#             return {
#                 "message": "Chat session updated for existing user.",
#                 "response": response_text,
#             }
#         else:
#             # User does not exist in the database
#             return {
#                 "message": "User not found in the database. Please register first.",
#                 "status": "error",
#             }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


