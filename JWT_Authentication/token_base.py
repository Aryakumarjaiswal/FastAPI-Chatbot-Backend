import time
import jwt
from app.JWT_Authentication.token_config import JWT_SECRET, JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60  # 1 hour
REFRESH_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 7  # 7 days

def create_jwt(user_id: str, role: str, is_refresh: bool = False) -> str:
    """
    Create a JWT token. Use 'is_refresh' to indicate a refresh token.
    """
    expiration = time.time() + (REFRESH_TOKEN_EXPIRE_SECONDS if is_refresh else ACCESS_TOKEN_EXPIRE_SECONDS)
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": expiration,
        "type": "refresh" if is_refresh else "access",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt(token: str):
    """
    Decode a JWT token and return the payload.
    """
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
