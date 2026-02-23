import feedparser
import asyncio
import os
from duckduckgo_search import DDGS
from telegram import Bot

# Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def get_quantum_news():
    print("Fetching news from Phys.org...")
    url = "https://phys.org/rss-feed/physics-news/quantum-physics/"
    feed = feedparser.parse(url)
    news_items = feed.entries[:3]
    
    if not news_items:
        return "പുതിയ വാർത്തകൾ ഒന്നും ലഭ്യമല്ല."

    combined_news = "\n".join([f"Title: {e.title}\nSummary: {e.summary}" for e in news_items])
    
    print("Connecting to Free AI (DuckDuckGo)...")
    try:
        # Gemini-ക്ക് പകരം സൗജന്യ AI ഉപയോഗിക്കുന്നു
        with DDGS() as ddgs:
            prompt = f"Summarize these Quantum Physics news into simple Malayalam bullet points:\n\n{combined_news}"
            results = ddgs.chat(prompt, model='gpt-4o-mini')
            return results
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return "AI പരിഭാഷയിൽ ഒരു ചെറിയ സാങ്കേതിക തടസ്സം."

async def send_to_telegram():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        news_malayalam = await get_quantum_news()
        
        print("Sending to Telegram...")
        await bot.send_message(
            chat_id=CHAT_ID, 
            text="⚛️ *ഇന്നത്തെ ക്വാണ്ടം വാർത്തകൾ*\n\n" + news_malayalam, 
            parse_mode='Markdown'
        )
        print("✅ SUCCESS!")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ Missing Secrets!")
    else:
        asyncio.run(send_to_telegram())
