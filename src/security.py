from passlib.context import CryptContext
import os
from datetime import datetime, timezone, timedelta
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_acess_token(data: dict):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire_time = now + timedelta(minutes=30)
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt