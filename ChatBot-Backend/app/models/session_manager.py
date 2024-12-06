from sqlalchemy.orm import Session
from app.database import Guest_ChatRecord,SessionLocal
from app.config import transfer_to_customer_service
from app.rag.rag_using_json1 import rag_using_json
db = SessionLocal()

class SessionManager:
    def __init__(self, model):
        self.model = model
        self.sessions = {}

    def get_chat_session(self, session_id: str):
        if session_id not in self.sessions:
            # Start a new chat session with the role as "model" for the system prompt
            self.sessions[session_id] = self.model.start_chat(history=[])
        return self.sessions[session_id]



    def send_message(
        self, session_id: str, message: str, name=None, email=None, phone_number=None
    ):
        chat_session = self.get_chat_session(session_id)

        prompt = rag_using_json(message=message)

        #print("prompt: ", prompt)

        response = chat_session.send_message(prompt)

        print("response: ", response)

        parts = response.candidates[0].content.parts
        #print(parts)
        response_text = ""

        for part in parts:

            # Check for the function call in the response part
            if (
                hasattr(part, "function_call")
                and part.function_call is not None
                and part.function_call.name == "transfer_to_customer_service" 
            ):
                
                transfer_to_customer_service(name,email,phone_number)

                # Extract function call arguments directly as a dictionary
                #try:
                    # Here, fn.args should work directly as a dictionary-like object
                    #args = {key: val for key, val in part.function_call.args.items()}
                    #print("Function call arguments:", args)
                #except AttributeError as e:
                #    print(f"Error extracting function call arguments: {e}")
                #    return "An error occurred while processing your request."


            elif hasattr(part, "text"):
                response_text += part.text
            print(response_text)



        print("response text ISSSS: ", response_text, "\n message: ISSSS ", message)
        return response_text







    # def send_message(
    #     self, session_id: str, message: str, name=None, email=None, phone_number=None
    # ):
    #     chat_session = self.get_chat_session(session_id)

    #     prompt = rag_using_json(message=message)

    #     print("prompt: ", prompt)

    #     response = chat_session.send_message(prompt)

    #     print("response: ", response)

    #     parts = response.candidates[0].content.parts
    #     print(parts)
    #     response_text = ""

    #     for part in parts:

    #         # Check for the function call in the response part
    #         if (
    #             hasattr(part, "function_call")
    #             and part.function_call is not None
    #             and part.function_call.name == "transfer_to_customer_service" 
    #         ):

    #             # Extract function call arguments directly as a dictionary
    #             #try:
    #                 # Here, fn.args should work directly as a dictionary-like object
    #                 #args = {key: val for key, val in part.function_call.args.items()}
    #                 #print("Function call arguments:", args)
    #             #except AttributeError as e:
    #             #    print(f"Error extracting function call arguments: {e}")
    #             #    return "An error occurred while processing your request."

    #             # Call the transfer function with extracted arguments
    #             transfer_response = transfer_to_customer_service(
    #                name=name,
    #                email=email,
    #                phone_number=phone_number,
    #             )

    #             # Save the transfer information in the database
    #             db = SessionLocal()
    #             self.save_chat_record(
    #                 db,
    #                 session_id,
    #                 user_message=message,
    #                 model_response=response_text,
    #                 name=name,
    #                 email=email,
    #                 phone_number=phone_number,
    #             )
    #             db.close()

    #             return transfer_response

    #         elif hasattr(part, "text"):
    #             response_text += part.text
    #             print(response_text)

    #     # Save regular response text if no function call was detected
    #     db = SessionLocal()
    #     self.save_chat_record(
    #         db,
    #         session_id,
    #         user_message=message,
    #         model_response=response_text,
    #     )
    #     db.close()

    #     print("response text: ", response_text, "\n message: ", message)
    #     return response_text
