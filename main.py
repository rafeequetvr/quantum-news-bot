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

if not TELEGRAM_TOKEN or not GEMINI_API_KEY or not CHAT_ID:
    print("Error: Missing secrets!")
    sys.exit(1)

# പുതിയ ക്ലയന്റ് സെറ്റപ്പ്
client = genai.Client(api_key=GEMINI_API_KEY)

async def get_quantum_news():
    url = "https://phys.org/rss-feed/physics-news/quantum-physics/"
    feed = feedparser.parse(url)
    news_items = feed.entries[:3]
    
    if not news_items:
        return "ഇന്ന് പുതിയ വാർത്തകൾ ഒന്നും റിപ്പോർട്ട് ചെയ്തിട്ടില്ല."

    combined_news = ""
    for entry in news_items:
        combined_news += f"Title: {entry.title}\nSummary: {entry.summary}\n\n"
    
    prompt = f"Summarize these Quantum Physics news into simple Malayalam bullet points:\n\n{combined_news}"
    
    # മോഡൽ നെയിം 'gemini-1.5-flash-latest' എന്ന് മാറ്റി
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI പരിഭാഷയിൽ ഒരു പ്രശ്നം സംഭവിച്ചു: {e}"

async def send_to_telegram():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        news_malayalam = await get_quantum_news()
        message = "⚛️ *ഇന്നത്തെ ക്വാണ്ടം വാർത്തകൾ*\n\n" + news_malayalam
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
        print("Success! News sent to Telegram.")
    except Exception as e:
        print(f"Error during Telegram send: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(send_to_telegram())
