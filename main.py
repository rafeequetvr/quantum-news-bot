import feedparser
import google.generativeai as genai
import asyncio
import os
import sys
from telegram import Bot

# പരിസ്ഥിതി ചരങ്ങൾ (Environment Variables) സുരക്ഷിതമായി എടുക്കുന്നു
TELEGRAM_TOKEN = os.getenv(8579546992:AAHumr2OPn9DyRamkqUTIJ8RPaKyX32Nu6Q)
GEMINI_API_KEY = os.getenv(AIzaSyAd65Dgqtn4tilMwWR-9pYu3NgwnuOTF40)
CHAT_ID = os.getenv(1328852027)

# ടോക്കണുകൾ ഉണ്ടോ എന്ന് പരിശോധിക്കുന്നു (Error Handling)
if not TELEGRAM_TOKEN or not GEMINI_API_KEY or not CHAT_ID:
    print("Error: One or more secrets (TELEGRAM_TOKEN, GEMINI_API_KEY, CHAT_ID) are missing!")
    sys.exit(1)

# Gemini AI സെറ്റപ്പ്
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_quantum_news():
    url = "https://phys.org/rss-feed/physics-news/quantum-physics/"
    feed = feedparser.parse(url)
    news_items = feed.entries[:3]
    
    if not news_items:
        return "പുതിയ വാർത്തകൾ ഒന്നും ലഭ്യമല്ല."

    combined_news = ""
    for entry in news_items:
        combined_news += f"Title: {entry.title}\nSummary: {entry.summary}\n\n"
    
    prompt = f"Summarize these Quantum Physics news into simple Malayalam bullet points:\n\n{combined_news}"
    response = model.generate_content(prompt)
    return response.text

async def send_to_telegram():
    try:
        bot = Bot(token=8579546992:AAHumr2OPn9DyRamkqUTIJ8RPaKyX32Nu6Q)
        news_malayalam = await get_quantum_news()
        await bot.send_message(chat_id=CHAT_ID, text="⚛️ *ഇന്നത്തെ ക്വാണ്ടം വാർത്തകൾ*\n\n" + news_malayalam, parse_mode='Markdown')
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(send_to_telegram())
