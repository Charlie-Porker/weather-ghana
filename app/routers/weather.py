from fastapi import APIRouter, HTTPException

import requests

router = APIRouter(prefix="/weather")

@router.get("/{city}")

def get_weather(city):
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
    return {"city": city, "temperature": temp}