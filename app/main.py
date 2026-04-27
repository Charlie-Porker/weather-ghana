from fastapi import FastAPI
from app.routers import weather
from app.database import engine, Base

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(weather.router)

@app.get("/")
def root():
    return {
        "message": "Welcome"
    } 