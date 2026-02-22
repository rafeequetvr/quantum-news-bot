import feedparser
import asyncio
import os
import sys
from google import genai
from telegram import Bot

# Secrets എടുക്കുന്നു
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

async def get_quantum_news():
    print("Fetching news from Phys.org...")
    url = "https://phys.org/rss-feed/physics-news/quantum-physics/"
    feed = feedparser.parse(url)
    news_items = feed.entries[:3]
    
    if not news_items:
        return "പുതിയ വാർത്തകൾ ഒന്നും ലഭ്യമല്ല."

    combined_news = ""
    for entry in news_items:
        combined_news += f"Title: {entry.title}\nSummary: {entry.summary}\n\n"
    
    print("Sending to Gemini AI for translation...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        models/gemini-1.5-flash, 
        contents=f"Summarize these Quantum Physics news into simple Malayalam bullet points:\n\n{combined_news}"
    )
    return response.text

async def send_to_telegram():
    try:
        print(f"Connecting to Telegram Bot... (Chat ID: {CHAT_ID})")
        bot = Bot(token=TELEGRAM_TOKEN)
        
        news_malayalam = await get_quantum_news()
        
        print("Sending message to Telegram...")
        await bot.send_message(
            chat_id=CHAT_ID, 
            text="⚛️ *ഇന്നത്തെ ക്വാണ്ടം വാർത്തകൾ*\n\n" + news_malayalam, 
            parse_mode='Markdown'
        )
        print("✅ SUCCESS: Message sent to Telegram!")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        # എറർ വന്നാൽ പ്രോഗ്രാം നിർത്താതിരിക്കാൻ sys.exit ഒഴിവാക്കി

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY or not CHAT_ID:
        print("❌ ERROR: Missing Secrets in GitHub Settings!")
    else:
        asyncio.run(send_to_telegram())
