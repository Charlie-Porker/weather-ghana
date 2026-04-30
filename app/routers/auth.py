from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserData
from pydantic import BaseModel
from app.database import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

router = APIRouter(prefix="/auth")

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

@router.post("/register")
def NewUser(payload: UserRegister,
            db=Depends(get_db)):
        nam = db.query(UserData).filter(UserData.username == payload.username).first()
        if nam:
              raise HTTPException(status_code=409, detail="Username already exists")        
        else:
              new_user = UserData(
                    username=payload.username,
                    email=payload.email,
                    password=pwd_context.hash(payload.password)
              )
              db.add(new_user)
              db.commit()
              return {
                    "Mess": "User Created"
              }