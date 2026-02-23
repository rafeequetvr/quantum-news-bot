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
    
    print("Connecting to Gemini via Stable REST API (v1)...")
    
    # മാറ്റം ഇവിടെയാണ്: v1beta എന്നതിന് പകരം v1 എന്ന് നൽകുന്നു
    api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Summarize these Quantum Physics news into simple Malayalam bullet points:\n\n{combined_news}"}]
        }]
    }

    try:
        response = requests.post(api_url, json=payload)
        result = response.json()
        
        # എറർ ഉണ്ടോ എന്ന് ചെക്ക് ചെയ്യുന്നു
        if "error" in result:
            print(f"❌ API Error Details: {result['error']['message']}")
            return "AI വാർത്തകൾ തയ്യാറാക്കുന്നതിൽ ഒരു സാങ്കേതിക പ്രശ്നം നേരിട്ടു."
            
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"❌ Script Error: {e}")
        return "വാർത്തകൾ പരിഭാഷപ്പെടുത്താൻ സാധിച്ചില്ല."

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
    asyncio.run(send_to_telegram())
