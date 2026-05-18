from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import user as user_crud
from app.schemas.auth import UserCreate, UserLogin, UserResponse, Token
from app.core import security

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(deps.get_db)):
    user = user_crud.get_user_by_phone(db, phone=user_in.phone)
    if user:
        raise HTTPException(status_code=400, detail="Bu telefon raqami allaqachon ro'yxatdan o'tgan")
    return user_crud.create_user(db, user_in=user_in)

@router.post("/register-admin", response_model=UserResponse)
def register_admin(user_in: UserCreate, db: Session = Depends(deps.get_db)):
    user = user_crud.get_user_by_phone(db, phone=user_in.phone)
    if user:
        raise HTTPException(status_code=400, detail="Bu telefon raqami allaqachon ro'yxatdan o'tgan")
    
    # Force admin and seller roles for this endpoint
    db_user = user_crud.create_user(db, user_in=user_in)
    db_user.is_admin = True
    db_user.is_seller = True
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(deps.get_db)):
    user = user_crud.get_user_by_phone(db, phone=user_in.phone)
    if not user or not security.verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Telefon raqami yoki parol noto'g'ri")
    
    access_token = security.create_access_token(subject=user.phone)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(deps.get_current_user)):
    return current_user
