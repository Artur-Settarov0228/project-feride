from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

def get_products(db: Session, category: str = None, search: str = None, seller_id: int = None):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if search:
        query = query.filter(Product.name.contains(search))
    if seller_id is not None:
        query = query.filter(Product.seller_id == seller_id)
    return query.all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

from app.models.category import Category

def get_categories(db: Session):
    return db.query(Category).all()

def create_product(db: Session, product_in: ProductCreate):
    db_product = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        old_price=product_in.old_price,
        image_url=product_in.image_url,
        category=product_in.category,
        rating=product_in.rating,
        reviews_count=product_in.reviews_count,
        badge=product_in.badge,
        delivery_info=product_in.delivery_info,
        seller_id=product_in.seller_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product
