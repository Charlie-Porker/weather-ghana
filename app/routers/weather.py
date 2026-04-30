from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.models import WeatherCache
from datetime import datetime
from pydantic import BaseModel

import requests
class WeatherUpdate(BaseModel):
    temperature: float

router = APIRouter(prefix="/weather")

@router.get("/")
def get_all():
    db = SessionLocal()
    all_city = db.query(WeatherCache).all()
    return all_city  

@router.put("/{city}")
def upda_city(city,
              payload: WeatherUpdate):
    db = SessionLocal()
    up_city = db.query(WeatherCache).filter(WeatherCache.city == city).first()
    if not up_city:
        raise HTTPException(status_code=404, detail="City not found")
    else:
        up_city.temperature = payload.temperature
        up_city.time = datetime.utcnow()
        db.commit()
    return {
        "ma": "done updating"
    }

@router.delete("/{city}")
def del_city(city):
    db = SessionLocal()
    del_one = db.query(WeatherCache).filter(WeatherCache.city == city).first()
    if not del_one:
        raise HTTPException(status_code=404, detail="city not found")
    else:
        db.delete(del_one)
        db.commit()
    return {
        "mess": "success" 
    }        

@router.get("/{city}")
def get_weather(city):
    db = SessionLocal()
    cached = db.query(WeatherCache).filter(WeatherCache.city == city).first()
    if cached:
        age = datetime.utcnow() - cached.time
        if age.seconds < 1800:  # 1800 seconds = 30 minutes
            return {"city": city, "temperature": cached.temperature, "source": "cache"}
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(url)
    data = response.json()
    if not data.get("results"):
        raise HTTPException(status_code=404, detail="city not found")
    lats = data["results"][0]["latitude"]
    lons = data["results"][0]["longitude"]
    wea_url = f"https://api.open-meteo.com/v1/forecast?latitude={lats}&longitude={lons}&current_weather=true"
    wea_response = requests.get(wea_url)
    wea_data = wea_response.json()
    temp = wea_data["current_weather"]["temperature"]
    if cached:
        cached.temperature = temp
        cached.time = datetime.utcnow()
    else:
        new_cache = WeatherCache(city=city, temperature=temp, time=datetime.utcnow())
        db.add(new_cache)

    db.commit()
    return {"city": city, "temperature": temp}


