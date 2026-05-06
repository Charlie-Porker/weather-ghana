from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

oauth2_scheme = HTTPBearer()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_token(username: str):
    expiry = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": username, "exp": expiry}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload =  jwt.decode(token.credentials, SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        return username
    except:
        raise HTTPException(status_code=401, detail="invalid token")