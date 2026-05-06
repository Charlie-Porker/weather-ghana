from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_token(username: str):
    expiry = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": username, "exp": expiry}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token