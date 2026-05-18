from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    phone: Optional[str] = None

class UserBase(BaseModel):
    phone: str
    full_name: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str
    is_seller: Optional[bool] = False
    is_admin: Optional[bool] = False

class UserLogin(BaseModel):
    phone: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_seller: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
