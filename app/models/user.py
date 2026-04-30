from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database import Base


class UserData(Base):
    __tablename__ =  "user_data"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)