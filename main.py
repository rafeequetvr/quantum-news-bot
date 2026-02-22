import feedparser
import google.generativeai as genai
import asyncio
import os
import sys
from telegram import Bot

# ശരിയായ രീതിയിൽ കോട്ടേഷൻ മാർക്കിനുള്ളിൽ (Quotes) പേര് നൽകുന്നു
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

# പരിശോധന: കീ കൾ ലഭ്യമാണോ എന്ന് നോക്കുന്നു
if not TELEGRAM_TOKEN or not GEMINI_API_KEY or not CHAT_ID:
    print("Error: Missing secrets! Check GitHub Settings.")
    sys.exit(1)

# Gemini AI സെറ്റപ്പ്
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_quantum_news():
    url = "https://phys.org/rss-feed/physics-news/quantum-physics/"
    feed = feedparser.parse(url)
    news_items = feed.entries[:3]
    
    if not news_items:
        return "പുതിയ വാർത്തകൾ ഒന്നും ലഭ്യമല്ല."

    combined_news = ""
    for entry in news_items:
        combined_news += f"Title: {entry.title}\nSummary: {entry.summary}\n\n"
    
    prompt = f"Summarize these Quantum Physics news into simple Malayalam bullet points:\n\n{combined_news}"
    response = model.generate_content(prompt)
    return response.text

async def send_to_telegram():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        news_malayalam = await get_quantum_news()
        await bot.send_message(chat_id=CHAT_ID, text="⚛️ *ഇന്നത്തെ ക്വാണ്ടം വാർത്തകൾ*\n\n" + news_malayalam, parse_mode='Markdown')
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(send_to_telegram())
