import feedparser
import asyncio
import os
import requests
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
    
    if not news_items:
        return "പുതിയ വാർത്തകൾ ഒന്നും ലഭ്യമല്ല."

    combined_news = "\n".join([f"Title: {e.title}\nSummary: {e.summary}" for e in news_items])
    
    print("Connecting to Gemini via REST API...")
    # പുതിയ SDK പ്രശ്നമുണ്ടാക്കുന്നതുകൊണ്ട് നേരിട്ട് REST API ഉപയോഗിക്കുന്നു
    # ഈ വരി മാത്രം ശ്രദ്ധിച്ച് മാറ്റുക
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Summarize these Quantum Physics news into simple Malayalam bullet points:\n\n{combined_news}"}]
        }]
    }

    try:
        response = requests.post(api_url, json=payload)
        result = response.json()
        # AI നൽകുന്ന മറുപടി എടുക്കുന്നു
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"❌ AI Error: {e}\nResponse: {response.text}")
        return "AI വാർത്തകൾ തയ്യാറാക്കുന്നതിൽ ഒരു തടസ്സം നേരിട്ടു."

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
    asyncio.run(send_to_telegram())
