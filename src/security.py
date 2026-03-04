from passlib.context import CryptContext
import os
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from fastapi.security import APIKeyHeader
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
import database, models

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

oauth2_scheme = APIKeyHeader(name="Authorization")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Não foi possível validar suas credenciais. Faça login novamente!",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()

    if user is None:
        raise credentials_exception
    
    return user