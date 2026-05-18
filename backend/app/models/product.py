from sqlalchemy import Column, Integer, String, Float, Text
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    old_price = Column(Float, nullable=True)
    image_url = Column(String(500), nullable=True)
    category = Column(String(100), index=True)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    badge = Column(String(50), nullable=True) # e.g., "Xit savdo", "Yangi"
    delivery_info = Column(String(100), default="Ertaga")
    seller_id = Column(Integer, nullable=True) # Nullable for older seeded products if needed
