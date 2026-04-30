from fastapi import FastAPI
from app.routers import weather, auth
from app.database import engine, Base
from app.models.user import UserData

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(weather.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {
        "message": "Welcome"
    } 