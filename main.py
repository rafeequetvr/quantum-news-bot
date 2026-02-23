import feedparser
import asyncio
import os
import sys
from google import genai
from telegram import Bot

# Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

async def get_quantum_news():
    print("Fetching news...")
    url = "https://phys.org/rss-feed/physics-news/quantum-physics/"
    feed = feedparser.parse(url)
    news_items = feed.entries[:3]
    
    if not news_items: return "വാർത്തകൾ ലഭ്യമല്ല."

    combined_news = "\n".join([f"{e.title}: {e.summary}" for e in news_items])
    
    # പുതിയ ക്ലയന്റ് കോൺഫിഗറേഷൻ
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    try:
        # നേരിട്ട് മോഡൽ പേര് നൽകുന്നു
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=f"Summarize these news into simple Malayalam bullet points:\n\n{combined_news}"
        )
        return response.text
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return "AI പരിഭാഷയിൽ പ്രശ്നമുണ്ട്. API Key ശരിയാണോ എന്ന് പരിശോധിക്കുക."

async def send_to_telegram():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        news_malayalam = await get_quantum_news()
        print("Sending to Telegram...")
        await bot.send_message(chat_id=CHAT_ID, text="⚛️ *ഇന്നത്തെ ക്വാണ്ടം വാർത്തകൾ*\n\n" + news_malayalam, parse_mode='Markdown')
        print("✅ SUCCESS!")
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

if __name__ == "__main__":
    if not all([TELEGRAM_TOKEN, GEMINI_API_KEY, CHAT_ID]):
        print("❌ Missing Secrets!")
    else:
        asyncio.run(send_to_telegram())
