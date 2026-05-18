from pydantic import BaseModel
from app.schemas.product import ProductResponse

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(CartItemBase):
    id: int
    product: ProductResponse

    class Config:
        from_attributes = True
class CheckoutRequest(BaseModel):
    name: str
    phone: str
    location: str
