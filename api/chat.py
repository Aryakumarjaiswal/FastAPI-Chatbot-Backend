from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import model
from fastapi.security import HTTPBearer
from app.database import SessionLocal,Guest_ChatRecord,hash_password,verify_password
from app.models.session_manager import SessionManager
from app.JWT_Authentication.token_base import create_jwt,decode_jwt
from app.rag.rag_using_json1 import rag_using_json
router = APIRouter()
session_manager = SessionManager(model=model)


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

auth_scheme = HTTPBearer()

def get_current_user(auth: str = Depends(auth_scheme)):
    """
    Validate JWT and return user payload.
    """
    token = auth.credentials
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload
@router.post("/refresh-token")
async def refresh_token(refresh_token: str):
    """
    Generate a new access token using a valid refresh token.
    """
    payload = decode_jwt(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    # Create a new access token
    access_token = create_jwt(user_id=payload["user_id"], role=payload["role"])
    return {"access_token": access_token}
@router.post("/chat(Guest)")
async def chat(session_id: str, message: str, name: str = None, email: str = None, db: Session = Depends(get_db)):
    try:
        print(f"Incoming parameters: session_id={session_id}, message={message}, name={name}, email={email}")
        
        # Validate user details
        user = db.query(Guest_ChatRecord).filter_by(name=name, email=email).first()
        print("USERRRRR CHECKING DONE")
        if not user:
            raise HTTPException(status_code=400, detail="User not found. Please register.")
        
        # Update session and log messages
        user.session_id = session_id
        response_text = session_manager.send_message(session_id, message, name, email)
        user.user_message = (user.user_message or "") + f"\n USER-> {message}"
        user.model_response = (user.model_response or "") + f"\n RESPONSE-> {response_text}"
        
        # Commit changes to the database
        db.commit()
        db.refresh(user)
        
        return {"session_id": session_id, "response": response_text}
    
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error. Please try again.")



@router.post("/Login")
async def login(name: str, email: str,password : str,db: Session = Depends(get_db)):
   
    try:
       
        user = db.query(Guest_ChatRecord).filter_by(email=email).first()
        if user and  verify_password(password,user.password):

        #return {"message": f"{name} Logged In Successfully!!"}
            access_token = create_jwt(user_id=str(user.user_id), role=user.Role)
            refresh_token = create_jwt(user_id=str(user.user_id), role=user.Role, is_refresh=True)

            return {
                "message": "Login successful!",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

        
        else:
            return {"message": f"Please Enter Valid Credentials!!!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.post('/Sign-Up')
async def registered_user(name: str, email: str, mob_no: str,password:str,Repeat_password:str, db: Session = Depends(get_db)):
    """Function for Registered User"""
    try:
        if password != Repeat_password:
            return "Your Password is not matching"
        hashed_password=hash_password(password)
        user = db.query(Guest_ChatRecord).filter_by(name=name,password=hashed_password,email=email).first()
       
        if not user:
            # Add new user if not already registered
            new_user = Guest_ChatRecord(name=name, email=email,password=hashed_password,Role="GUEST",phone_number=mob_no)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {"message": f"User {name} has been Registered In successfully!"}

        return {"message": f"Welcome back, {name}! You are an authorized registered user!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")






@router.post('/ChatTeam')
async def chat_team(
    session_id: str,
    message: str,
    Press1forGuest2forRegistered:str=1,
    name: str = None,
    email: str = None,
    phone_number: str = None,
    db: Session = Depends(get_db)
):
    """Function for Chat Support Team"""
    try:
        
        user = db.query(Guest_ChatRecord).filter_by(name=name, email=email, phone_number=phone_number).first()
        
           
        # Validate user details
        

        if user:
            # User exists in the database
            # Append the chat session details to transfer_call columns
            user.transfer_call_user_message = (
                (user.transfer_call_user_message or "") + f"\n USER-> {message}"
            )
            
            # Generate model response
            chat_session = session_manager.get_chat_session(session_id)
            prompt = rag_using_json(message=message)
            response = chat_session.send_message(prompt)
            response_text = "\n\n\n".join(
                part.text for part in response.candidates[0].content.parts if hasattr(part, "text")
            )
            print(response_text)

            user.transfer_call_response = (
               (user.transfer_call_response or "") + f"\n RESPONSE-> {response_text}"
            )
            print(user.transfer_call_response)
            db.commit()
            db.refresh(user)

            return {
                "message": "Chat session updated for existing user.",
                "response": response_text,
            }
        else:
            # User does not exist in the database
            return {
                "message": "User not found in the database. Please register first.",
                "status": "error",
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/retrieve_history")
async def show_history(
    name: str,
    email: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)  # Protect with JWT validation
):
    """
    Protected endpoint to retrieve user history.
    """
    user_record = db.query(Guest_ChatRecord).filter_by(name=name, email=email).first()
    if user_record:
        return {
            "User_Name": user_record.name,
            "E-Mail": user_record.email,
            "Session_ID": user_record.session_id,
            "AI_Conversation_History": {
                "User Query": user_record.user_message,
                "AI Response": user_record.model_response,
            },
        }
    return {"message": "User not found"}
