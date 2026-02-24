import feedparser
import asyncio
import os
from groq import Groq
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LAST_LINK_FILE = "last_link_crude.txt"

def get_last_link():
    if os.path.exists(LAST_LINK_FILE):
        with open(LAST_LINK_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_last_link(link):
    with open(LAST_LINK_FILE, "w") as f:
        f.write(link)

async def get_crude_oil_news():
    print("Fetching Crude Oil news...")
    urls = [
        "https://feeds.reuters.com/reuters/businessNews",
        "https://www.investing.com/rss/news_25.rss",
        "https://feeds.feedburner.com/oilprice-latest-energy-news",
    ]
    latest_entry = None
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title_lower = entry.title.lower()
            if any(word in title_lower for word in ["crude", "oil", "opec", "brent", "wti", "petroleum"]):
                latest_entry = entry
                break
        if latest_entry:
            break

    if not latest_entry:
        print("No crude oil news found.")
        return None, None

    latest_link = latest_entry.link
    last_link = get_last_link()

    if latest_link == last_link:
        print("No new news found.")
        return None, None

    print("New crude oil news found! Connecting to Groq AI...")
    try:
        client = Groq(api_key=GROQ_API_KEY)
        summary = getattr(latest_entry, 'summary', latest_entry.title)
        content = f"Title: {latest_entry.title}\nSummary: {summary}"
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": f"""You are a crude oil trading analyst. Analyze this news and provide a summary in Malayalam with the following format:

📰 വാർത്ത സംഗ്രഹം:
(2-3 lines summary in Malayalam)

📈 വിപണി സ്വാധീനം:
(Will crude oil price go UP or DOWN? Explain in Malayalam)

💡 Trading Signal:
(BUY / SELL / NEUTRAL - with reason in Malayalam)

News: {content}"""
            }],
            max_tokens=600
        )
        return response.choices[0].message.content, latest_link
    except Exception as e:
        print(f"AI Error: {e}")
        return None, None

async def send_to_telegram():
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        news_malayalam, latest_link = await get_crude_oil_news()
        if news_malayalam:
            print("Sending to Telegram...")
            await bot.send_message(
                chat_id=CHAT_ID,
                text="🛢️ *ക്രൂഡ് ഓയിൽ വാർത്ത*\n\n" + news_malayalam,
                parse_mode='Markdown'
            )
            save_last_link(latest_link)
            print("SUCCESS!")
        else:
            print("Everything is up to date.")
    except Exception as e:
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not CHAT_ID or not GROQ_API_KEY:
        print("Missing Secrets!")
    else:
        asyncio.run(send_to_telegram())
