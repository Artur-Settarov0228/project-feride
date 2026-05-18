from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.schemas.auth import UserResponse, UserCreate
from app.crud import user as user_crud

router = APIRouter()

def check_admin(current_user: User = Depends(deps.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@router.get("/stats", dependencies=[Depends(check_admin)])
def get_stats(db: Session = Depends(deps.get_db)):
    user_count = db.query(User).count()
    product_count = db.query(Product).count()
    category_count = db.query(Category).count()
    
    # Simple recent activity (last 5 users)
    recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
    
    return {
        "users": user_count,
        "products": product_count,
        "categories": category_count,
        "recent_users": [
            {
                "id": u.id, 
                "full_name": u.full_name, 
                "phone": u.phone, 
                "created_at": u.created_at,
                "is_admin": u.is_admin,
                "is_seller": u.is_seller
            }
            for u in recent_users
        ]
    }

@router.get("/users", response_model=List[UserResponse], dependencies=[Depends(check_admin)])
def get_all_users(db: Session = Depends(deps.get_db)):
    return db.query(User).all()

@router.post("/users", response_model=UserResponse, dependencies=[Depends(check_admin)])
def create_managed_user(user_in: UserCreate, db: Session = Depends(deps.get_db)):
    user = user_crud.get_user_by_phone(db, phone=user_in.phone)
    if user:
        raise HTTPException(status_code=400, detail="Bu telefon raqami allaqachon ro'yxatdan o'tgan")
    
    # In managed user creation, we respect the is_seller flag and manually set is_admin if needed
    # (Actually we could add is_admin to UserCreate if we wanted, but let's handle it here)
    db_user = user_crud.create_user(db, user_in=user_in)
    
    # If the user_in doesn't have is_admin, we can decide based on context or add it to schema
    # For now, let's assume the frontend can specify if it's an admin or seller
    return db_user

@router.delete("/users/{user_id}", dependencies=[Depends(check_admin)])
def delete_user(user_id: int, db: Session = Depends(deps.get_db)):
    if user_id == 1:
        raise HTTPException(status_code=400, detail="Asosiy adminni o'chirib bo'lmaydi")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    
    db.delete(user)
    db.commit()
    return {"message": "Foydalanuvchi muvaffaqiyatli o'chirildi"}
