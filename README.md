# FastAPI-Chatbot-Backend
All endpoints are working smooth.
![image](https://github.com/user-attachments/assets/c9293db7-bcc5-48f9-837f-4a138a99afe3)


A sophisticated AI-powered chatbot backend built with FastAPI and Google's Gemini AI, featuring RAG (Retrieval-Augmented Generation) capabilities and JWT authentication.

## 🌟 Features

- **AI-Powered Chat**: Integration with Google's Gemini AI model
- **RAG Implementation**: Enhanced responses using context from JSON data
- **Authentication**: JWT-based authentication with refresh token support
- **User Management**: Support for both guest and registered users
- **Chat History**: Persistent storage of chat conversations
- **Database Integration**: MySQL database using SQLAlchemy ORM
- **API Security**: Bearer token authentication for protected endpoints

## 🛠 Tech Stack

- FastAPI
- Google Gemini AI
- SQLAlchemy
- PyJWT
- Pandas
- NumPy
- MySQL
- Python 3.x

## 📁 Project Structure
![image](https://github.com/user-attachments/assets/0a7ac7a0-c664-45a3-801b-c2cc0f5e1fca)

## 🚀 Getting Started

1. **Clone the repository**
```plaintext
git clone <repository-url>
cd FastAPI-Chatbot-Backend
```


2. **Set up virtual environment**
In IDE Terminal let say VSCode run below
```plaintext
python -m venv MyVenv
MyVenv\Scripts\activate.bat (windows)
```

3. **Install dependencies**
```plaintext
pip install -r requirements.txt
```

4. **Configure environment variables**
- Set up your GEMINI_API_KEY
- Configure MySQL database connection

5. **Initialize the database**
```plaintext
python database.py
```

6. **Run the application**
```plaintext
uvicorn main:app --reload
```

## 🔑 API Endpoints

- `POST /chat(Guest)`: Chat endpoint for guest users
- `POST /Login`: User authentication endpoint
- `POST /Sign-Up`: User registration endpoint
- `POST /ChatTeam`: Support team chat endpoint
- `GET /retrieve_history`: Retrieve chat history (protected)
- `POST /refresh-token`: Get new access token using refresh token

## 💾 Database Schema

The main table `GUEST_RECORDS` includes:
- user_id (Primary Key)
- session_id
- user_message
- model_response
- name
- email
- phone_number
- password
- Role
- transfer_call_user_message

## 🔒 Security

- JWT-based authentication with access and refresh tokens
- Password hashing using bcrypt
- Bearer token authentication for protected endpoints
- Environment variable protection for sensitive data

## 📝 License

[Add your license information here]

## 👥 Contact

For support or queries, please contact:
Email:aryakumarofficial830@gmail.com

