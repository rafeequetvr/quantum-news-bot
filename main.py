import feedparser
import asyncio
import os
import google.generativeai as genai
from telegram import Bot

# Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def get_quantum_news():
    print("Fetching news from Phys.org...")
    url = "https://phys.org/rss-feed/physics-news/quantum-physics/"
    feed = feedparser.parse(url)
    news_items = feed.entries[:3]

    if not news_items:
        return "പുതിയ വാർത്തകൾ ഒന്നും ലഭ്യമല്ല."

    combined_news = "\n".join([f"Title: {e.title}\nSummary: {e.summary}" for e in news_items])

    print("Connecting to Gemini AI...")
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"Summarize these Quantum Physics news into simple Malayalam bullet points. Focus on key details:\n\n{combined_news}"

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"❌ AI Error: {e}")
        return "AI വാർത്തകൾ തയ്യാറാക്കുന്നതിൽ ഒരു സാങ്കേതിക പ്രശ്നം നേരിട്ടു."

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
    if not TELEGRAM_TOKEN or not CHAT_ID or not GEMINI_API_KEY:
        print("❌ Missing Secrets!")
    else:
        asyncio.run(send_to_telegram())
```

---

**requirements.txt ഇങ്ങനെ ആക്കുക:**
```
feedparser
python-telegram-bot
google-generativeai
