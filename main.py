import feedparser
import asyncio
import os
from groq import Groq
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def get_quantum_news():
    print("Fetching news from Phys.org...")
    url = "https://phys.org/rss-feed/physics-news/quantum-physics/"
    feed = feedparser.parse(url)
    news_items = feed.entries[:3]

    if not news_items:
        return "പുതിയ വാർത്തകൾ ഒന്നും ലഭ്യമല്ല."

    combined_news = "\n".join([f"Title: {e.title}\nSummary: {e.summary}" for e in news_items])

    print("Connecting to Groq AI...")
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Summarize these Quantum Physics news into simple Malayalam bullet points. Focus on key details:\n\n{combined_news}"}],
            max_tokens=500
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"AI Error: {e}")
        return "AI വാർത്തകൾ തയ്യാറാക്കുന്നതിൽ ഒരു സാങ്കേതിക പ്രശ്നം നേരിട്ടു."

async def send_to_telegram():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        news_malayalam = await get_quantum_news()
        print("Sending to Telegram...")
        await bot.send_message(
            chat_id=CHAT_ID,
            text="⚛️ ഇന്നത്തെ ക്വാണ്ടം വാർത്തകൾ\n\n" + news_malayalam,
        )
        print("SUCCESS!")
    except Exception as e:
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not CHAT_ID or not GROQ_API_KEY:
        print("Missing Secrets!")
    else:
        asyncio.run(send_to_telegram())
