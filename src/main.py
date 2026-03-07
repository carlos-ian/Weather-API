from fastapi import FastAPI
from database import Base, engine
import models

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

from auth_routes import auth_router
from weather_routes import weather_router

app.include_router(auth_router)
app.include_router(weather_router)

from fastapi.responses import FileResponse
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get("/")
async def read_login():
    login_path = os.path.join(BASE_DIR, "frontend", "login.html")
    return FileResponse(login_path)

@app.get("/index.html")
async def read_index():
    index_path = os.path.join(BASE_DIR, "frontend", "index.html")
    return FileResponse(index_path)