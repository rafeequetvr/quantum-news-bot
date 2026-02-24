import feedparser
import asyncio
import os
from groq import Groq
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# അവസാനമായി അയച്ച വാർത്തയുടെ ലിങ്ക് സൂക്ഷിക്കുന്ന ഫയൽ
LAST_LINK_FILE = "last_link.txt"

def get_last_link():
    if os.path.exists(LAST_LINK_FILE):
        with open(LAST_LINK_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_last_link(link):
    with open(LAST_LINK_FILE, "w") as f:
        f.write(link)

async def get_quantum_news():
    print("Fetching news from Phys.org...")
    url = "https://phys.org/rss-feed/physics-news/quantum-physics/"
    feed = feedparser.parse(url)
    
    if not feed.entries:
        return None, None

    latest_entry = feed.entries[0] # ഏറ്റവും പുതിയ വാർത്ത
    latest_link = latest_entry.link
    last_link = get_last_link()

    # പുതിയ വാർത്തയാണോ എന്ന് നോക്കുന്നു
    if latest_link == last_link:
        print("No new news found.")
        return None, None

    print("New news found! Connecting to Groq AI...")
    try:
        client = Groq(api_key=GROQ_API_KEY)
        content = f"Title: {latest_entry.title}\nSummary: {latest_entry.summary}"
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"Summarize this Quantum Physics news into simple Malayalam (max 3-4 bullet points):\n\n{content}"}],
            max_tokens=500
        )
        return response.choices[0].message.content, latest_link

    except Exception as e:
        print(f"AI Error: {e}")
        return None, None

async def send_to_telegram():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        news_malayalam, latest_link = await get_quantum_news()
        
        if news_malayalam:
            print("Sending new update to Telegram...")
            await bot.send_message(
                chat_id=CHAT_ID,
                text="⚛️ *പുതിയ ക്വാണ്ടം വാർത്ത*\n\n" + news_malayalam,
                parse_mode='Markdown'
            )
            save_last_link(latest_link) # ലിങ്ക് സേവ് ചെയ്യുന്നു
            print("SUCCESS!")
        else:
            print("Everything is up to date.")
    except Exception as e:
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    asyncio.run(send_to_telegram())
