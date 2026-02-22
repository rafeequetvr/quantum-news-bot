import feedparser
import google.generativeai as genai
import asyncio
import os
import sys
from telegram import Bot

# ശരിയായ രീതിയിൽ രഹസ്യനാമങ്ങൾ എടുക്കുന്നു
TELEGRAM_TOKEN = os.getenv(8579546992:AAHumr2OPn9DyRamkqUTIJ8RPaKyX32Nu6Q)
GEMINI_API_KEY = os.getenv(AIzaSyAd65Dgqtn4tilMwWR-9pYu3NgwnuOTF40)
CHAT_ID = os.getenv(1328852027)

# പരിശോധന: ഏതെങ്കിലും കീ കുറവാണെങ്കിൽ പ്രോഗ്രാം ഇവിടെ നിർത്തും
if not TELEGRAM_TOKEN or not GEMINI_API_KEY or not CHAT_ID:
    print(f"Error: Missing secrets! TG: {bool(TELEGRAM_TOKEN)}, AI: {bool(GEMINI_API_KEY)}, ID: {bool(CHAT_ID)}")
    sys.exit(1)

# Gemini AI സെറ്റപ്പ്
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_quantum_news():
    url = "https://phys.org/rss-feed/physics-news/quantum-physics/"
    feed = feedparser.parse(url)
    news_items = feed.entries[:3]
    
    if not news_items:
        return "ഇന്ന് പുതിയ വാർത്തകൾ ഒന്നും റിപ്പോർട്ട് ചെയ്തിട്ടില്ല."

    combined_news = ""
    for entry in news_items:
        combined_news += f"Title: {entry.title}\nSummary: {entry.summary}\n\n"
    
    prompt = f"Summarize these Quantum Physics news into simple Malayalam bullet points:\n\n{combined_news}"
    response = model.generate_content(prompt)
    return response.text

async def send_to_telegram():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        news_malayalam = await get_quantum_news()
        message = "⚛️ *ഇന്നത്തെ ക്വാണ്ടം വാർത്തകൾ*\n\n" + news_malayalam
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
        print("Telegram message sent!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(send_to_telegram())
