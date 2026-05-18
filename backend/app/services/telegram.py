import httpx
from app.core.config import settings
import html

async def send_telegram_order(name: str, phone: str, location: str, items: list, total_price: float):
    # O'zingizning bot ma'lumotlaringizni kiriting
    BOT_TOKEN = "8763636405:AAGY8yAcNyFKnjNQEl9TY4-M4rrbCJDMpOE"
    CHAT_ID = "1402478160"
    
    # Escape user inputs for HTML to prevent formatting errors
    safe_name = html.escape(str(name))
    safe_phone = html.escape(str(phone))
    safe_location = html.escape(str(location))
    
    message = f"🌟 <b>YANGI BUYURTMA — MASION FERIDE</b>\n"
    message += f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
    message += f"👤 <b>Mijoz:</b> {safe_name}\n"
    message += f"📞 <b>Telefon:</b> <code>{safe_phone}</code>\n"
    message += f"📍 <b>Manzil:</b> {safe_location}\n\n"
    message += f"📦 <b>Mahsulotlar ro'yxati:</b>\n"
    
    for i, item in enumerate(items, 1):
        safe_product_name = html.escape(str(item['product']['name']))
        size_str = f" (Razmer: {html.escape(str(item['size']))})" if item.get('size') else ""
        message += f"{i}. <b>{safe_product_name}</b>{size_str}\n"
        message += f"   └ {item['quantity']} dona × {item['product']['price']:,} so'm\n"

    
    message += f"\n💰 <b>UMUMIY SUMMA:</b> <code>{total_price:,}</code> so'm\n"
    message += f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
    message += f"🕒 <i>Vaqti: {settings.PROJECT_NAME} Order System</i>"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    SITE_URL = "http://172.29.24.251:3000" 
    
    reply_markup = {
        "inline_keyboard": [[
            {"text": "🌐 Saytga o'tish", "url": SITE_URL},
            {"text": "✅ Tasdiqlash", "callback_data": "confirm_order"}
        ]]
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "reply_markup": reply_markup
            })
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"Telegram HTTP error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"Telegram error: {e}")

