import asyncio
import httpx

BOT_TOKEN = "8763636405:AAGY8yAcNyFKnjNQEl9TY4-M4rrbCJDMpOE"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

async def poll_updates():
    offset = 0
    print("🤖 Telegram bot polling started (Listening for Tasdiqlash button)...")
    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            try:
                response = await client.get(f"{API_URL}/getUpdates", params={"offset": offset, "timeout": 20})
                data = response.json()
                updates = data.get("result", [])
                for update in updates:
                    offset = update["update_id"] + 1
                    if "callback_query" in update:
                        cb = update["callback_query"]
                        if cb.get("data") == "confirm_order":
                            cb_id = cb["id"]
                            # Answer the callback query to stop the loading spinner
                            await client.post(f"{API_URL}/answerCallbackQuery", json={
                                "callback_query_id": cb_id, 
                                "text": "✅ Buyurtma qabul qilindi va tasdiqlandi!",
                                "show_alert": True
                            })
                            
                            # Edit the message to show it is confirmed
                            if "message" in cb:
                                chat_id = cb["message"]["chat"]["id"]
                                message_id = cb["message"]["message_id"]
                                
                                # Use the HTML formatting for the edit
                                # We remove the inline keyboard by sending empty reply_markup
                                await client.post(f"{API_URL}/editMessageReplyMarkup", json={
                                    "chat_id": chat_id,
                                    "message_id": message_id,
                                    "reply_markup": {"inline_keyboard": []} # Remove buttons
                                })
                                
                                # Optionally append text
                                text = cb["message"].get("text", "") or cb["message"].get("caption", "")
                                new_text = text + "\n\n✅ <b>HOLATI: TASDIQLANGAN</b>"
                                await client.post(f"{API_URL}/editMessageText", json={
                                    "chat_id": chat_id,
                                    "message_id": message_id,
                                    "text": new_text,
                                    "parse_mode": "HTML"
                                })
                                print(f"Order confirmed for message {message_id}")
                    
                    elif "message" in update:
                        msg = update["message"]
                        if msg.get("text") == "/start":
                            chat_id = msg["chat"]["id"]
                            await client.post(f"{API_URL}/sendMessage", json={
                                "chat_id": chat_id,
                                "text": "👋 <b>Masion Feride botiga xush kelibsiz!</b>\n\nBu yerda siz saytdan kelgan buyurtmalarni qabul qilasiz va tasdiqlashingiz mumkin.",
                                "parse_mode": "HTML"
                            })
            except Exception as e:
                print(f"Bot update error: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(poll_updates())
    except KeyboardInterrupt:
        print("Bot stopped.")
