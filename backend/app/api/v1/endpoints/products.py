from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.crud import product as product_crud
from app.schemas.product import ProductResponse, ProductCreate

router = APIRouter()

@router.post("/", response_model=ProductResponse)
def create_product(
    product_in: ProductCreate,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    if not current_user.is_seller and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    product_in.seller_id = current_user.id
    return product_crud.create_product(db, product_in=product_in)

@router.get("/", response_model=List[ProductResponse])
def get_products(
    db: Session = Depends(deps.get_db),
    category: Optional[str] = None,
    search: Optional[str] = None,
    seller_id: Optional[int] = None
):
    return product_crud.get_products(db, category=category, search=search, seller_id=seller_id)

@router.get("/categories")
def get_categories(db: Session = Depends(deps.get_db)):
    return product_crud.get_categories(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(deps.get_db)):
    product = product_crud.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    current_user = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    product = product_crud.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Only admin or the seller who owns the product can delete it
    if not current_user.is_admin and product.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges to delete this product")
    
    product_crud.delete_product(db, product_id=product_id)
    return {"detail": "Product deleted successfully"}
