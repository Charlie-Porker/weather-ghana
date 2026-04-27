from sqlalchemy import Column, String, Float, DateTime, Integer
from app.database import Base


class WeatherCache(Base):
    __tablename__ = "weather_cache"
    
    id = Column(Integer, primary_key=True)
    city = Column(String, unique=True)
    temperature = Column(Float)
    time = Column(DateTime)