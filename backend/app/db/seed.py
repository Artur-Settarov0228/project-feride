from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.product import Product
from app.models.user import User
from app.models.cart import CartItem

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_products():
    db = SessionLocal()
    # Clear old products for the new theme
    db.query(Product).delete()
    
    products = [
        # Tashqi kiyim
        Product(
            name="Klassik Trenchkot",
            description="Bahor mavsumi uchun ideal tanlov. Suvga chidamli mato.",
            price=1250000,
            old_price=1500000,
            image_url="https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500&q=80",
            category="Tashqi kiyim",
            rating=4.9,
            reviews_count=28,
            badge="Yangi"
        ),
        Product(
            name="Oversize Kurtka",
            description="Zamonaviy va issiq kurtka, har qanday kiyim bilan mos tushadi.",
            price=950000,
            old_price=1100000,
            image_url="https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=500&q=80",
            category="Tashqi kiyim",
            rating=4.8,
            reviews_count=15
        ),
        # Trikotaj
        Product(
            name="Yumshoq Kasmir Svitshot",
            description="Tabiiy kasmirdan ishlangan juda yumshoq svitshot.",
            price=650000,
            old_price=800000,
            image_url="https://images.unsplash.com/photo-1556905055-8f358a7a4bb4?w=500&q=80",
            category="Trikotaj",
            rating=5.0,
            reviews_count=42,
            badge="Xit savdo"
        ),
        Product(
            name="Trikotaj Kostyum-Shim",
            description="Uyda va ko'chada kiyish uchun qulay to'plam.",
            price=750000,
            old_price=900000,
            image_url="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=500&q=80",
            category="Trikotaj",
            rating=4.7,
            reviews_count=19
        ),
        # Tolstovkalar
        Product(
            name="Baza Xudi",
            description="Har kunlik kiyish uchun qalin va sifatli xudi.",
            price=450000,
            old_price=550000,
            image_url="https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&q=80",
            category="Tolstovkalar",
            rating=4.6,
            reviews_count=65
        ),
        # Kiyim (General)
        Product(
            name="Oq Paxtali Ko'ylak",
            description="Ofis uchun klassik oq ko'ylak, 100% paxta.",
            price=350000,
            old_price=450000,
            image_url="https://images.unsplash.com/photo-1598033129183-c4f50c717658?w=500&q=80",
            category="Kiyim",
            rating=4.9,
            reviews_count=31
        ),
        # Pidjak va kurtkalar
        Product(
            name="Klassik Pidjak",
            description="Nafis dizayn va yuqori sifatli mato.",
            price=850000,
            old_price=1000000,
            image_url="https://images.unsplash.com/photo-1548624313-0396c75e4b1a?w=500&q=80",
            category="Pidjak va kurtkalar",
            rating=4.8,
            reviews_count=12
        ),
        # Bluzkalar va ko'ylaklar
        Product(
            name="Ipakli Bluzka",
            description="Kechki uchrashuvlar uchun nafis ipakli bluzka.",
            price=550000,
            old_price=700000,
            image_url="https://images.unsplash.com/photo-1612336307429-8a898d10e223?w=500&q=80",
            category="Bluzkalar va ko'ylaklar",
            rating=4.7,
            reviews_count=24
        ),
        Product(
            name="Elegant Kechki Ko'ylak",
            description="Maxsus kechalar uchun ipakli va nafis ko'ylak.",
            price=1850000,
            old_price=2200000,
            image_url="https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500&q=80",
            category="Bluzkalar va ko'ylaklar",
            rating=5.0,
            reviews_count=8,
            badge="Premium"
        )
    ]
    
    db.add_all(products)
    db.commit()
    print("Muvaffaqiyatli: 9 ta yangi premium mahsulot qo'shildi!")

if __name__ == "__main__":
    seed_products()
