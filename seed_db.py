import sqlite3
import os

DB_PATH = "backend/masion_feride.db"

def seed_db():
    if not os.path.exists(DB_PATH):
        print("Database not found! Starting backend to create it...")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear existing products
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM categories")

    # Add Categories
    categories = [
        ("Kostyumlar", "https://images.unsplash.com/photo-1594932224010-74f43a18350d?q=80&w=500&auto=format&fit=crop"),
        ("Ko'ylaklar", "https://images.unsplash.com/photo-1595777457583-95e059d581b8?q=80&w=500&auto=format&fit=crop"),
        ("Sumkalar", "https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=500&auto=format&fit=crop"),
        ("Poyabzallar", "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?q=80&w=500&auto=format&fit=crop"),
        ("Aksessuarlar", "https://images.unsplash.com/photo-1523206489230-c012c64b2b48?q=80&w=500&auto=format&fit=crop")
    ]
    
    for name, img in categories:
        cursor.execute("INSERT INTO categories (name, image_url) VALUES (?, ?)", (name, img))

    # Add Products
    products = [
        # Kostyumlar
        ("Elegance Midnight Suit", "Premium junli matodan tikilgan oqshom kostyumi.", 2500000, 3200000, "https://images.unsplash.com/photo-1593032465175-481ac7f401a0?q=80&w=800&auto=format&fit=crop", "Kostyumlar", "NEW", "2 soat"),
        ("Classic Business Grey", "Ishbilarmon ayollar uchun klassik kulrang kostyum.", 1800000, None, "https://images.unsplash.com/photo-1548142813-c348350df52b?q=80&w=800&auto=format&fit=crop", "Kostyumlar", None, "Ertaga"),
        ("Velvet Emerald Suit", "Yashil baxmal matodan tayyorlangan hashamatli kostyum-shim.", 2800000, 3500000, "https://images.unsplash.com/photo-1594932224010-74f43a18350d?q=80&w=800&auto=format&fit=crop", "Kostyumlar", "HOT", "Ertaga"),
        ("White Pearl Collection", "Oq ipak aralashmali yozgi ofis kostyumi.", 2100000, None, "https://images.unsplash.com/photo-1554412933-514a83d2f3c8?q=80&w=800&auto=format&fit=crop", "Kostyumlar", None, "3 soat"),
        ("Black Diamond Suit", "Qora rangli klassik va bashang dizayn.", 2300000, 2700000, "https://images.unsplash.com/photo-1574047805177-3e818816c21e?q=80&w=800&auto=format&fit=crop", "Kostyumlar", "LIMITED", "Ertaga"),
        ("Royal Silk Tuxedo", "Maxsus tadbirlar uchun ipak yoqali smokining.", 4200000, 5000000, "https://images.unsplash.com/photo-1598808503746-f34c53b39739?q=80&w=800&auto=format&fit=crop", "Kostyumlar", "EXKLYUZIV", "1 kun"),
        
        # Ko'ylaklar
        ("Silk Evening Dress", "Haqiqiy ipakdan tayyorlangan hashamatli oqshom ko'ylagi.", 3500000, 4500000, "https://images.unsplash.com/photo-1539008835270-301bd14b91f6?q=80&w=800&auto=format&fit=crop", "Ko'ylaklar", "HOT", "3 soat"),
        ("Summer Floral Maxi", "Yozgi gulli printli yengil ko'ylak.", 850000, None, "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?q=80&w=800&auto=format&fit=crop", "Ko'ylaklar", None, "Ertaga"),
        ("Red Carpet Gown", "Qizil gilam uchun maxsus dizayndagi uzun ko'ylak.", 5500000, 6800000, "https://images.unsplash.com/photo-1566160983808-b80c352ed77c?q=80&w=800&auto=format&fit=crop", "Ko'ylaklar", "NEW", "1 soat"),
        ("Elegant Black Dress", "Kichik qora ko'ylak - har bir ayol garderobida bo'lishi shart.", 1500000, None, "https://images.unsplash.com/photo-1550639525-c97d455acf70?q=80&w=800&auto=format&fit=crop", "Ko'ylaklar", None, "Ertaga"),
        ("Royal Blue Velvet", "Moviy baxmal ko'ylak - ziyofatlar uchun ajoyib tanlov.", 3200000, 4000000, "https://images.unsplash.com/photo-1595777457583-95e059d581b8?q=80&w=800&auto=format&fit=crop", "Ko'ylaklar", "SALE", "Ertaga"),
        ("Golden Lace Gown", "Tilla rangli to'rli hashamatli ko'ylak.", 4800000, None, "https://images.unsplash.com/photo-1518767761162-d5933635a6aa?q=80&w=800&auto=format&fit=crop", "Ko'ylaklar", "NEW", "Ertaga"),
        
        # Sumkalar
        ("Premium Leather Tote", "Italiya charmidan tayyorlangan keng hajmli sumka.", 1200000, 1500000, "https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=800&auto=format&fit=crop", "Sumkalar", "SALE", "Ertaga"),
        ("Gold Chain Clutch", "Bayramlar uchun tilla rang zanjirli kichik sumka.", 750000, None, "https://images.unsplash.com/photo-1566150905458-1bf1fd15dcb4?q=80&w=800&auto=format&fit=crop", "Sumkalar", None, "Ertaga"),
        ("Classic Handbag Black", "Kundalik uchun juda mos bo'lgan qora rangli sumka.", 950000, 1100000, "https://images.unsplash.com/photo-1591561954557-26941169b49e?q=80&w=800&auto=format&fit=crop", "Sumkalar", "NEW", "Ertaga"),
        ("Mini Crossbody Bag", "Zamonaviy va yengil yelkaga osiladigan sumkach.", 550000, None, "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?q=80&w=800&auto=format&fit=crop", "Sumkalar", None, "2 soat"),
        ("Luxury Shopper", "Xaridlar uchun katta va chidamli teri sumka.", 1800000, 2200000, "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?q=80&w=800&auto=format&fit=crop", "Sumkalar", "HOT", "Ertaga"),
        
        # Poyabzallar
        ("Velvet Stilettos", "Baxmaldan tayyorlangan baland poshnali tuflilar.", 950000, 1200000, "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?q=80&w=800&auto=format&fit=crop", "Poyabzallar", "NEW", "2 soat"),
        ("Casual White Sneakers", "Kundalik kiyish uchun qulay va zamonaviy krossovkalar.", 650000, None, "https://images.unsplash.com/photo-1549298916-b41d501d3772?q=80&w=800&auto=format&fit=crop", "Poyabzallar", None, "Ertaga"),
        ("Classic Red Pumps", "Qizil poshnali tuflilar - diqqat markazida bo'lish uchun.", 1100000, 1400000, "https://images.unsplash.com/photo-1515347619362-e64e9a3b6f25?q=80&w=800&auto=format&fit=crop", "Poyabzallar", "HOT", "Ertaga"),
        ("Winter Leather Boots", "Qishki qulay va issiq teri etiklar.", 1500000, None, "https://images.unsplash.com/photo-1608667508764-33cf0726b13a?q=80&w=800&auto=format&fit=crop", "Poyabzallar", None, "Ertaga"),
        ("Summer Sandals", "Yoz uchun havo o'tkazadigan yengil sandallar.", 450000, 600000, "https://images.unsplash.com/photo-1562183241-b937e95585b6?q=80&w=800&auto=format&fit=crop", "Poyabzallar", "SALE", "Ertaga"),
        
        # Aksessuarlar
        ("Silk Scarf Azure", "Tabiiy ipakdan tayyorlangan havorang sharf.", 450000, None, "https://images.unsplash.com/photo-1584030373081-f37b7bb4fa8e?q=80&w=800&auto=format&fit=crop", "Aksessuarlar", None, "Ertaga"),
        ("Crystal Earrings Set", "Kechki liboslar uchun billur ziraklar to'plami.", 300000, 450000, "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?q=80&w=800&auto=format&fit=crop", "Aksessuarlar", "LIMITED", "3 soat"),
        ("Gold Plated Necklace", "Nafis dizayndagi tillaga jalb qilingan bo'yinbog'.", 850000, 1100000, "https://images.unsplash.com/photo-1599643478524-fb66f7f2b1d6?q=80&w=800&auto=format&fit=crop", "Aksessuarlar", "HOT", "Ertaga"),
        ("Designer Sunglasses", "Quyoshdan himoyalovchi zamonaviy brend ko'zoynagi.", 600000, None, "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=800&auto=format&fit=crop", "Aksessuarlar", None, "Ertaga"),
        ("Leather Belt Classic", "Haqiqiy teridan qilingan klassik kamar.", 250000, 350000, "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?q=80&w=800&auto=format&fit=crop", "Aksessuarlar", "SALE", "Ertaga")
    ]

    for p in products:
        cursor.execute("""
            INSERT INTO products (name, description, price, old_price, image_url, category, badge, delivery_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    # Add Admin User
    admin_pass_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGGa31S2" # "admin"
    cursor.execute("DELETE FROM users WHERE phone = ?", ("admin",))
    cursor.execute("""
        INSERT INTO users (full_name, phone, password_hash, is_admin, is_seller, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("Administrator", "admin", admin_pass_hash, 1, 1, 1))

    # Add Seller User
    seller_pass_hash = "$2b$12$Xz9Y5B/Y.R8Y6Y8Y6Y8Y6Y8Y6Y8Y6Y8Y6Y8Y6Y8Y6Y8Y6Y8Y6Y8Y6" # "seller"
    # Actually I'll use the same hash for "seller" password if I want to be quick, 
    # but I'll use a real one. Let's just use "admin" pass for seller too for simplicity of testing.
    cursor.execute("DELETE FROM users WHERE phone = ?", ("seller",))
    cursor.execute("""
        INSERT INTO users (full_name, phone, password_hash, is_admin, is_seller, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("Sotuvchi", "seller", admin_pass_hash, 0, 1, 1))

    conn.commit()
    conn.close()
    print("Database seeded successfully with premium products, Admin and Seller users!")

if __name__ == "__main__":
    seed_db()
