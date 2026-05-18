import os
import sys

# Crucial: Override DATABASE_URL to always point to backend/masion_feride.db relative to workspace root
# so that running this from either the root folder or the backend folder uses the exact same database.
os.environ["DATABASE_URL"] = "sqlite:///./backend/masion_feride.db"

# Add backend directory to sys.path to resolve imports correctly
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "backend"))

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models.user import User
from app.models.product import Product
from app.models.cart import CartItem
from app.models.category import Category

DB_PATH = "backend/masion_feride.db"

def seed_db():
    print("Deleting old database file to apply fresh schema...")
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("Old database deleted successfully.")
        except Exception as e:
            print(f"Could not remove DB file directly (might be locked): {e}. Dropping tables instead.")
            Base.metadata.drop_all(bind=engine)
            
    print("Creating all tables with latest schema...")
    Base.metadata.create_all(bind=engine)

    print("Seeding database using SQLAlchemy Session...")
    db = SessionLocal()
    try:
        # 1. Add Categories
        categories = [
            Category(name="Kostyumlar", image_url="https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?q=80&w=500&auto=format&fit=crop"),
            Category(name="Ko'ylaklar", image_url="https://images.unsplash.com/photo-1595777457583-95e059d581b8?q=80&w=500&auto=format&fit=crop"),
            Category(name="Sumkalar", image_url="https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=500&auto=format&fit=crop"),
            Category(name="Poyabzallar", image_url="https://images.unsplash.com/photo-1543163521-1bf539c55dd2?q=80&w=500&auto=format&fit=crop"),
            Category(name="Aksessuarlar", image_url="https://images.unsplash.com/photo-1523206489230-c012c64b2b48?q=80&w=500&auto=format&fit=crop")
        ]
        for cat in categories:
            db.add(cat)
        
        # 2. Add Products
        products = [
            # Kostyumlar (Women's sizes XS-XL)
            Product(
                name="Elegance Midnight Suit", 
                description="Premium junli matodan tikilgan oqshom kostyumi.", 
                price=2500000.0, 
                old_price=3200000.0, 
                image_url="https://images.unsplash.com/photo-1593032465175-481ac7f401a0?q=80&w=800&auto=format&fit=crop", 
                category="Kostyumlar", 
                badge="NEW", 
                delivery_info="2 soat", 
                sizes="XS, S, M, L, XL"
            ),
            Product(
                name="Classic Business Grey", 
                description="Ishbilarmon ayollar uchun klassik kulrang kostyum.", 
                price=1800000.0, 
                old_price=None, 
                image_url="https://images.unsplash.com/photo-1548142813-c348350df52b?q=80&w=800&auto=format&fit=crop", 
                category="Kostyumlar", 
                badge=None, 
                delivery_info="Ertaga", 
                sizes="S, M, L, XL"
            ),
            Product(
                name="Velvet Emerald Suit", 
                description="Yashil baxmal matodan tayyorlangan hashamatli kostyum-shim.", 
                price=2800000.0, 
                old_price=3500000.0, 
                image_url="https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?q=80&w=800&auto=format&fit=crop", 
                category="Kostyumlar", 
                badge="HOT", 
                delivery_info="Ertaga", 
                sizes="S, M, L"
            ),
            Product(
                name="White Pearl Collection", 
                description="Oq ipak aralashmali yozgi ofis kostyumi.", 
                price=2100000.0, 
                old_price=None, 
                image_url="https://images.unsplash.com/photo-1554412933-514a83d2f3c8?q=80&w=800&auto=format&fit=crop", 
                category="Kostyumlar", 
                badge=None, 
                delivery_info="3 soat", 
                sizes="XS, S, M, L"
            ),
            Product(
                name="Black Diamond Suit", 
                description="Qora rangli klassik va bashang dizayn.", 
                price=2300000.0, 
                old_price=2700000.0, 
                image_url="https://images.unsplash.com/photo-1539109136881-3be0616acf4b?q=80&w=800&auto=format&fit=crop", 
                category="Kostyumlar", 
                badge="LIMITED", 
                delivery_info="Ertaga", 
                sizes="S, M, L, XL"
            ),
            Product(
                name="Royal Silk Tuxedo", 
                description="Maxsus tadbirlar uchun ipak yoqali smokining.", 
                price=4200000.0, 
                old_price=5000000.0, 
                image_url="https://images.unsplash.com/photo-1509631179647-0177331693ae?q=80&w=800&auto=format&fit=crop", 
                category="Kostyumlar", 
                badge="EXKLYUZIV", 
                delivery_info="1 kun", 
                sizes="S, M, L"
            ),
            
            # Ko'ylaklar (Women's sizes XS-XL)
            Product(
                name="Silk Evening Dress", 
                description="Haqiqiy ipakdan tayyorlangan hashamatli oqshom ko'ylagi.", 
                price=3500000.0, 
                old_price=4500000.0, 
                image_url="https://images.unsplash.com/photo-1496747611176-843222e1e57c?q=80&w=800&auto=format&fit=crop", 
                category="Ko'ylaklar", 
                badge="HOT", 
                delivery_info="3 soat", 
                sizes="XS, S, M, L"
            ),
            Product(
                name="Summer Floral Maxi", 
                description="Yozgi gulli printli yengil ko'ylak.", 
                price=850000.0, 
                old_price=None, 
                image_url="https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?q=80&w=800&auto=format&fit=crop", 
                category="Ko'ylaklar", 
                badge=None, 
                delivery_info="Ertaga", 
                sizes="S, M, L, XL"
            ),
            Product(
                name="Red Carpet Gown", 
                description="Qizil gilam uchun maxsus dizayndagi uzun ko'ylak.", 
                price=5500000.0, 
                old_price=6800000.0, 
                image_url="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=800&auto=format&fit=crop", 
                category="Ko'ylaklar", 
                badge="NEW", 
                delivery_info="1 soat", 
                sizes="XS, S, M, L"
            ),
            Product(
                name="Elegant Black Dress", 
                description="Kichik qora ko'ylak - har bir ayol garderobida bo'lishi shart.", 
                price=1500000.0, 
                old_price=None, 
                image_url="https://images.unsplash.com/photo-1550639525-c97d455acf70?q=80&w=800&auto=format&fit=crop", 
                category="Ko'ylaklar", 
                badge=None, 
                delivery_info="Ertaga", 
                sizes="S, M, L"
            ),
            Product(
                name="Royal Blue Velvet", 
                description="Moviy baxmal ko'ylak - ziyofatlar uchun ajoyib tanlov.", 
                price=3200000.0, 
                old_price=4000000.0, 
                image_url="https://images.unsplash.com/photo-1595777457583-95e059d581b8?q=80&w=800&auto=format&fit=crop", 
                category="Ko'ylaklar", 
                badge="SALE", 
                delivery_info="Ertaga", 
                sizes="S, M, L, XL"
            ),
            Product(
                name="Golden Lace Gown", 
                description="Tilla rangli to'rli hashamatli ko'ylak.", 
                price=4800000.0, 
                old_price=None, 
                image_url="https://images.unsplash.com/photo-1566207274740-0f8cf6b7d5a5?q=80&w=800&auto=format&fit=crop", 
                category="Ko'ylaklar", 
                badge="NEW", 
                delivery_info="Ertaga", 
                sizes="XS, S, M, L"
            ),
            
            # Sumkalar (Bags do not require size selection)
            Product(
                name="Premium Leather Tote", 
                description="Italiya charmidan tayyorlangan keng hajmli sumka.", 
                price=1200000.0, 
                old_price=1500000.0, 
                image_url="https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=500&auto=format&fit=crop", 
                category="Sumkalar", 
                badge="SALE", 
                delivery_info="Ertaga", 
                sizes=None
            ),
            Product(
                name="Gold Chain Clutch", 
                description="Bayramlar uchun tilla rang zanjirli kichik sumka.", 
                price=750000.0, 
                old_price=None, 
                image_url="https://images.unsplash.com/photo-1618244972963-dbee1a7edc95?q=80&w=800&auto=format&fit=crop", 
                category="Sumkalar", 
                badge=None, 
                delivery_info="Ertaga", 
                sizes=None
            ),
            Product(
                name="Classic Handbag Black", 
                description="Kundalik uchun juda mos bo'lgan qora rangli sumka.", 
                price=950000.0, 
                old_price=1100000.0, 
                image_url="https://images.unsplash.com/photo-1591561954557-26941169b49e?q=80&w=500&auto=format&fit=crop", 
                category="Sumkalar", 
                badge="NEW", 
                delivery_info="Ertaga", 
                sizes=None
            ),
            Product(
                name="Mini Crossbody Bag", 
                description="Zamonaviy va yengil yelkaga osiladigan sumkach.", 
                price=550000.0, 
                old_price=None, 
                image_url="https://images.unsplash.com/photo-1590874103328-eac38a683ce7?q=80&w=500&auto=format&fit=crop", 
                category="Sumkalar", 
                badge=None, 
                delivery_info="2 soat", 
                sizes=None
            ),
            Product(
                name="Luxury Shopper", 
                description="Xaridlar uchun katta va chidamli teri sumka.", 
                price=1800000.0, 
                old_price=2200000.0, 
                image_url="https://images.unsplash.com/photo-1548036328-c9fa89d128fa?q=80&w=500&auto=format&fit=crop", 
                category="Sumkalar", 
                badge="HOT", 
                delivery_info="Ertaga", 
                sizes=None
            ),
            
            # Poyabzallar (Women's shoe sizes 36-40)
            Product(
                name="Velvet Stilettos", 
                description="Baxmaldan tayyorlangan baland poshnali tuflilar.", 
                price=950000.0, 
                old_price=1200000.0, 
                image_url="https://images.unsplash.com/photo-1543163521-1bf539c55dd2?q=80&w=500&auto=format&fit=crop", 
                category="Poyabzallar", 
                badge="NEW", 
                delivery_info="2 soat", 
                sizes="36, 37, 38, 39, 40"
            ),
            Product(
                name="Casual White Sneakers", 
                description="Kundalik kiyish uchun qulay va zamonaviy krossovkalar.", 
                price=650000.0, 
                old_price=None, 
                image_url="https://images.unsplash.com/photo-1549298916-b41d501d3772?q=80&w=500&auto=format&fit=crop", 
                category="Poyabzallar", 
                badge=None, 
                delivery_info="Ertaga", 
                sizes="36, 37, 38, 39, 40"
            ),
            Product(
                name="Classic Red Pumps", 
                description="Qizil poshnali tuflilar - diqqat markazida bo'lish uchun.", 
                price=1100000.0, 
                old_price=1400000.0, 
                image_url="https://images.unsplash.com/photo-1549298916-b41d501d3772?q=80&w=800&auto=format&fit=crop", 
                category="Poyabzallar", 
                badge="HOT", 
                delivery_info="Ertaga", 
                sizes="36, 37, 38, 39, 40"
            ),
            Product(
                name="Winter Leather Boots", 
                description="Qishki qulay va issiq teri etiklar.", 
                price=1500000.0, 
                old_price=None, 
                image_url="https://images.unsplash.com/photo-1608667508764-33cf0726b13a?q=80&w=500&auto=format&fit=crop", 
                category="Poyabzallar", 
                badge=None, 
                delivery_info="Ertaga", 
                sizes="37, 38, 39, 40"
            ),
            Product(
                name="Summer Sandals", 
                description="Yoz uchun havo o'tkazadigan yengil sandallar.", 
                price=450000.0, 
                old_price=600000.0, 
                image_url="https://images.unsplash.com/photo-1562183241-b937e95585b6?q=80&w=500&auto=format&fit=crop", 
                category="Poyabzallar", 
                badge="SALE", 
                delivery_info="Ertaga", 
                sizes="36, 37, 38, 39"
            ),
            
            # Aksessuarlar (Accessories do not require sizes)
            Product(
                name="Silk Scarf Azure", 
                description="Tabiiy ipakdan tayyorlangan havorang sharf.", 
                price=450000.0, 
                old_price=None, 
                image_url="https://images.unsplash.com/photo-1584030373081-f37b7bb4fa8e?q=80&w=500&auto=format&fit=crop", 
                category="Aksessuarlar", 
                badge=None, 
                delivery_info="Ertaga", 
                sizes=None
            ),
            Product(
                name="Crystal Earrings Set", 
                description="Kechki liboslar uchun billur ziraklar to'plami.", 
                price=300000.0, 
                old_price=450000.0, 
                image_url="https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?q=80&w=500&auto=format&fit=crop", 
                category="Aksessuarlar", 
                badge="LIMITED", 
                delivery_info="3 soat", 
                sizes=None
            ),
            Product(
                name="Gold Plated Necklace", 
                description="Nafis dizayndagi tillaga jalb qilingan bo'yinbog'.", 
                price=850000.0, 
                old_price=1100000.0, 
                image_url="https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=800&auto=format&fit=crop", 
                category="Aksessuarlar", 
                badge="HOT", 
                delivery_info="Ertaga", 
                sizes=None
            ),
            Product(
                name="Designer Sunglasses", 
                description="Quyoshdan himoyalovchi zamonaviy brend ko'zoynagi.", 
                price=600000.0, 
                old_price=None, 
                image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=500&auto=format&fit=crop", 
                category="Aksessuarlar", 
                badge=None, 
                delivery_info="Ertaga", 
                sizes=None
            ),
            Product(
                name="Leather Belt Classic", 
                description="Haqiqiy teridan qilingan klassik kamar.", 
                price=250000.0, 
                old_price=350000.0, 
                image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?q=80&w=500&auto=format&fit=crop", 
                category="Aksessuarlar", 
                badge="SALE", 
                delivery_info="Ertaga", 
                sizes=None
            )
        ]
        for prod in products:
            db.add(prod)
        
        # 3. Add Admin User
        admin_pass_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGGa31S2" # "admin"
        admin_user = User(
            full_name="Administrator", 
            phone="admin", 
            password_hash=admin_pass_hash, 
            is_admin=True, 
            is_seller=True, 
            is_active=True
        )
        db.add(admin_user)
        
        # 4. Add Seller User
        seller_user = User(
            full_name="Sotuvchi", 
            phone="seller", 
            password_hash=admin_pass_hash, 
            is_admin=False, 
            is_seller=True, 
            is_active=True
        )
        db.add(seller_user)
        
        db.commit()
        print("Database seeded successfully with premium products, Admin and Seller users!")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
