import feedparser
import asyncio
import os
from google import genai
from telegram import Bot

# Secrets
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

    combined_news = "\n".join([f"Title: {e.title}\nSummary: {e.summary}" for e in news_items])
    
    print("Connecting to Gemini AI using NEW SDK...")
    # പുതിയ SDK ക്ലയന്റ്
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    try:
        # ഇവിടെ models/ എന്ന പ്രിഫിക്സ് ഇല്ലാതെ നൽകുന്നു
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=f"Summarize these Quantum Physics news into simple Malayalam bullet points:\n\n{combined_news}"
        )
        return response.text
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return "AI പരിഭാഷയിൽ പ്രശ്നം നേരിട്ടു. API Key അല്ലെങ്കിൽ Model ശരിയാണോ എന്ന് പരിശോധിക്കുക."

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
    if not all([TELEGRAM_TOKEN, GEMINI_API_KEY, CHAT_ID]):
        print("❌ Missing Secrets in GitHub Settings!")
    else:
        asyncio.run(send_to_telegram())
