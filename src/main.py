from fastapi import FastAPI
from database import Base, engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

from auth_routes import auth_router

app.include_router(auth_router)