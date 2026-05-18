from sqlalchemy.orm import Session
from app.models.cart import CartItem
from app.schemas.cart import CartItemCreate

def get_cart_items(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()

def add_to_cart(db: Session, user_id: int, item_in: CartItemCreate):
    existing = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == item_in.product_id
    ).first()
    
    if existing:
        existing.quantity += item_in.quantity
        db.commit()
        db.refresh(existing)
        return existing
    
    new_item = CartItem(
        user_id=user_id,
        product_id=item_in.product_id,
        quantity=item_in.quantity
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def update_cart_item(db: Session, user_id: int, item_id: int, quantity: int):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user_id).first()
    if item:
        item.quantity = quantity
        db.commit()
        db.refresh(item)
    return item

def delete_cart_item(db: Session, user_id: int, item_id: int):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item

def clear_cart(db: Session, user_id: int):
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()

def decrement_cart_item(db: Session, user_id: int, product_id: int):
    item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()
    
    if item:
        if item.quantity > 1:
            item.quantity -= 1
            db.commit()
            db.refresh(item)
            return item
        else:
            db.delete(item)
            db.commit()
            return None
    return None
