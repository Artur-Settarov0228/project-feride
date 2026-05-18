from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud import cart as cart_crud
from app.schemas.cart import CartItemCreate, CartItemResponse, CartItemUpdate, CheckoutRequest
from app.models.user import User
from app.services.telegram import send_telegram_order

router = APIRouter()

@router.post("/checkout")
async def checkout(
    request: CheckoutRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    items = cart_crud.get_cart_items(db, user_id=current_user.id)
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate total
    total = sum(item.product.price * item.quantity for item in items)
    
    # Format items for telegram
    items_data = []
    for item in items:
        items_data.append({
            "product": {"name": item.product.name, "price": item.product.price},
            "quantity": item.quantity
        })
    
    # Send to Telegram
    await send_telegram_order(
        name=request.name,
        phone=request.phone,
        location=request.location,
        items=items_data,
        total_price=total
    )
    
    # Clear cart
    cart_crud.clear_cart(db, user_id=current_user.id)
    
    return {"detail": "Order placed successfully", "bot_url": "https://t.me/YourBotName"}

@router.get("/", response_model=List[CartItemResponse])
def get_cart(current_user: User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    return cart_crud.get_cart_items(db, user_id=current_user.id)

@router.post("/", response_model=CartItemResponse)
def add_to_cart(
    item_in: CartItemCreate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    return cart_crud.add_to_cart(db, user_id=current_user.id, item_in=item_in)

@router.put("/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: int,
    item_in: CartItemUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    item = cart_crud.update_cart_item(db, user_id=current_user.id, item_id=item_id, quantity=item_in.quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item

@router.delete("/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    item = cart_crud.delete_cart_item(db, user_id=current_user.id, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"detail": "Item removed from cart"}
@router.delete("/")
def clear_cart(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    cart_crud.clear_cart(db, user_id=current_user.id)
    return {"detail": "Cart cleared"}

@router.post("/decrement/{product_id}")
def decrement_cart_item(
    product_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    item = cart_crud.decrement_cart_item(db, user_id=current_user.id, product_id=product_id)
    return {"detail": "Item quantity decreased", "item": item}
