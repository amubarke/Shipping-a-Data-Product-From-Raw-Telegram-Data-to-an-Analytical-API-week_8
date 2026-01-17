import os
import csv
import json
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import MessageMediaPhoto

# ============================
# Load environment variables
# ============================
load_dotenv()
API_ID = int(os.getenv("TELEGRAM_API_ID", "31964097"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "0b1cfe0051223911587b0ec5443be0c8")

# ============================
# CONFIGURATION
# ============================
CHANNELS = [
    "CheMed123",
    "tikvahpharma",
    "lobelia4cosmetics",
    "doctorfasil"
]

MAX_MESSAGES_PER_CHANNEL = 2000
TEXT_LIMIT = 1500
CHANNEL_DELAY_SECONDS = 20
MESSAGE_DELAY_SECONDS = 1
RATE_LIMIT_SLEEP = 60

# ============================
# PATHS
# ============================
BASE_DATA_DIR = "data/raw"
IMAGE_DIR = os.path.join(BASE_DATA_DIR, "images")
MESSAGE_DIR = os.path.join(BASE_DATA_DIR, "telegram_messages")
CSV_MESSAGE_DIR = "data/csv/telegram_messages"
STATE_DIR = "state"
LOG_DIR = "logs"

for d in [IMAGE_DIR, MESSAGE_DIR, CSV_MESSAGE_DIR, STATE_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

# ============================
# LOGGING
# ============================
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "scraper.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ============================
# TELEGRAM CLIENT
# ============================
client = TelegramClient(
    session="telegram_scraper",
    api_id=API_ID,
    api_hash=API_HASH
)

# ============================
# STATE MANAGEMENT
# ============================
def get_last_scrape_date(channel):
    path = os.path.join(STATE_DIR, f"{channel}_last_date.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return datetime.fromisoformat(json.load(f)["last_date"])
    return None

def save_last_scrape_date(channel, date):
    path = os.path.join(STATE_DIR, f"{channel}_last_date.json")
    with open(path, "w") as f:
        json.dump({"last_date": date.isoformat()}, f)

# ============================
# DATA STORAGE
# ============================
def save_messages_json(messages, date_str, channel):
    date_path = os.path.join(MESSAGE_DIR, date_str)
    os.makedirs(date_path, exist_ok=True)
    with open(os.path.join(date_path, f"{channel}.json"), "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def save_messages_csv(messages, date_str, channel):
    if not messages:
        return
    date_path = os.path.join(CSV_MESSAGE_DIR, date_str)
    os.makedirs(date_path, exist_ok=True)
    file_path = os.path.join(date_path, f"{channel}.csv")
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=messages[0].keys())
        writer.writeheader()
        writer.writerows(messages)

async def download_image(message, channel):
    channel_dir = os.path.join(IMAGE_DIR, channel)
    os.makedirs(channel_dir, exist_ok=True)
    image_path = os.path.join(channel_dir, f"{message.id}.jpg")
    await message.download_media(file=image_path)
    return image_path

# ============================
# SCRAPER
# ============================
async def scrape_channel(channel):
    logging.info(f"Scraping channel: {channel}")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    messages_data = []

    offset_date = get_last_scrape_date(channel)
    latest_message_date = offset_date
    message_count = 0

    try:
        async for message in client.iter_messages(
            channel,
            offset_date=offset_date,
            limit=MAX_MESSAGES_PER_CHANNEL
        ):
            if message_count >= MAX_MESSAGES_PER_CHANNEL:
                break

            message_count += 1
            await asyncio.sleep(MESSAGE_DELAY_SECONDS)

            has_media = message.media is not None

            image_path = None
            if isinstance(message.media, MessageMediaPhoto):
                image_path = await download_image(message, channel)

            msg = {
                "channel_name": channel,                      
                "message_id": message.id,
                "date": message.date.isoformat() if message.date else None,
                "text": (message.text or "")[:TEXT_LIMIT],
                "views": message.views,
                "forwards": message.forwards,
                "has_media": has_media,
                "image_path": image_path,
                        
            }

            messages_data.append(msg)

            if message.date:
                latest_message_date = max(
                    latest_message_date or message.date,
                    message.date
                )

        if messages_data:
            save_messages_json(messages_data, today, channel)
            save_messages_csv(messages_data, today, channel)
            save_last_scrape_date(channel, latest_message_date)

        logging.info(
            f"Completed {channel}: {message_count} messages"
        )

    except FloodWaitError as e:
        logging.warning(f"FloodWaitError for {channel}: sleeping {e.seconds}s")
        await asyncio.sleep(e.seconds + RATE_LIMIT_SLEEP)

    except Exception as e:
        logging.error(f"Error scraping {channel}: {str(e)}")

# ============================
# MAIN LOOP
# ============================
async def main():
    for channel in CHANNELS:
        await scrape_channel(channel)
        logging.info(f"Waiting {CHANNEL_DELAY_SECONDS}s before next channel")
        await asyncio.sleep(CHANNEL_DELAY_SECONDS)

# ============================
# ENTRY POINT
# ============================
with client:
    client.loop.run_until_complete(main())
