from pydantic import BaseModel
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    old_price: Optional[float] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = 0.0
    reviews_count: Optional[int] = 0
    badge: Optional[str] = None
    delivery_info: str = "Ertaga"
    seller_id: Optional[int] = None
    sizes: Optional[str] = None


class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True

class CategoryList(BaseModel):
    categories: List[str]
