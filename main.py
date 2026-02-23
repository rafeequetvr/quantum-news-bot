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
    
    print("Connecting to Gemini AI...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # നിങ്ങളുടെ കീയിൽ ലഭ്യമായ മോഡലുകൾ ലിസ്റ്റ് ചെയ്ത് അതിൽ നിന്ന് ഒന്ന് തിരഞ്ഞെടുക്കുന്നു
    available_model = "gemini-1.5-flash" # Default
    try:
        for m in client.models.list():
            if 'generateContent' in m.supported_methods:
                available_model = m.name
                break
        print(f"Using available model: {available_model}")
    except:
        print("Could not list models, using default.")

    try:
        response = client.models.generate_content(
            model=available_model, 
            contents=f"Summarize these news into simple Malayalam bullet points:\n\n{combined_news}"
        )
        return response.text
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return "AI വാർത്തകൾ തയ്യാറാക്കുന്നതിൽ ഒരു സാങ്കേതിക പ്രശ്നം. ഉടൻ പരിഹരിക്കും."

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
        print("❌ Missing Secrets!")
    else:
        asyncio.run(send_to_telegram())
