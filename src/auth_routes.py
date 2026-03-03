from fastapi import APIRouter, Depends, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
from security import get_password_hash, verify_password, create_acess_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user_exists = db.query(models.User).filter(models.User.username == user.username).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Este email já está cadastrado")
    
    hashed_password = get_password_hash(user.password)
        
    new_user = models.User (
        username = user.username,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário criado com sucesso", "username": new_user.username}

@auth_router("/login")
def login(user: schemas.UserSchema, db: Session = Depends(database.get_db)):
    user_exists = db.query(models.User).filter(models.User.username == user.username).first()
    if not user_exists or not verify_password(user.password, user_exists.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    token = create_acess_token(data={"sub": user_exists.email})
    return {"access_token": token, "token_type": "bearer"}