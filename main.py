import feedparser
import google.generativeai as genai
import asyncio
import os
from telegram import Bot

# GitHub Secrets-ൽ നിന്നുള്ള വിവരങ്ങൾ
TELEGRAM_TOKEN = os.getenv('8579546992:AAHumr2OPn9DyRamkqUTIJ8RPaKyX32Nu6Q')
GEMINI_API_KEY = os.getenv('AIzaSyAd65Dgqtn4tilMwWR-9pYu3NgwnuOTF40')
CHAT_ID = os.getenv('1328852027')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_quantum_news():
    url = "https://phys.org/rss-feed/physics-news/quantum-physics/"
    feed = feedparser.parse(url)
    news_items = feed.entries[:3]
    combined_news = ""
    for entry in news_items:
        combined_news += f"Title: {entry.title}\nSummary: {entry.summary}\n\n"
    
    prompt = f"Summarize these Quantum Physics news into simple Malayalam points:\n\n{combined_news}"
    response = model.generate_content(prompt)
    return response.text

async def send_to_telegram():
    bot = Bot(token=TELEGRAM_TOKEN)
    news_malayalam = await get_quantum_news()
    await bot.send_message(chat_id=CHAT_ID, text="⚛️ *ഇന്നത്തെ ക്വാണ്ടം വാർത്തകൾ*\n\n" + news_malayalam, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(send_to_telegram())
