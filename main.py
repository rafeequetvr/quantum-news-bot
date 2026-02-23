import feedparser
import asyncio
import os
import google.generativeai as genai
from telegram import Bot

# Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

# AI കോൺഫിഗറേഷൻ
genai.configure(api_key=GEMINI_API_KEY)

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
        # ഏറ്റവും സ്റ്റേബിൾ ആയ മോഡൽ വേർഷൻ
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            f"Summarize these Quantum Physics news into simple Malayalam bullet points:\n\n{combined_news}"
        )
        return response.text
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return "AI പരിഭാഷയിൽ ഒരു ചെറിയ സാങ്കേതിക പ്രശ്നം. ഉടൻ ശരിയാക്കാം!"

async def send_to_telegram():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        news_malayalam = await get_quantum_news()
        
        print("Sending to Telegram...")
        # മെസേജ് അയക്കുന്നു
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
