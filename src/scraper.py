import os
import json
import asyncio
from datetime import datetime
from pathlib import Path

from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
from loguru import logger

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_LAKE = BASE_DIR / "data" / "raw"
IMAGE_DIR = DATA_LAKE / "images"
MESSAGE_DIR = DATA_LAKE / "telegram_messages"
LOG_DIR = BASE_DIR / "logs" / "scraping"

LOG_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
MESSAGE_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Logging
# --------------------------------------------------
logger.add(
    LOG_DIR / "scraper.log",
    rotation="5 MB",
    level="INFO",
    format="{time} | {level} | {message}"
)

# --------------------------------------------------
# Telegram Channels
# --------------------------------------------------
CHANNELS = {
    "chemed": "https://t.me/chemed",
    "lobelia_cosmetics": "https://t.me/lobelia4cosmetics",
    "tikvah_pharma": "https://t.me/tikvahpharma"
}

# --------------------------------------------------
# Scraper Logic
# --------------------------------------------------
async def scrape_channel(client, channel_name, channel_url):
    logger.info(f"Starting scrape for channel: {channel_name}")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    output_dir = MESSAGE_DIR / today
    output_dir.mkdir(parents=True, exist_ok=True)

    messages_data = []

    async for message in client.iter_messages(channel_url, limit=500):
        msg = {
            "message_id": message.id,
            "channel_name": channel_name,
            "message_date": message.date.isoformat() if message.date else None,
            "message_text": message.text,
            "views": message.views,
            "forwards": message.forwards,
            "has_media": message.media is not None,
            "image_path": None
        }

        # Download images
        if isinstance(message.media, MessageMediaPhoto):
            channel_img_dir = IMAGE_DIR / channel_name
            channel_img_dir.mkdir(parents=True, exist_ok=True)

            image_path = channel_img_dir / f"{message.id}.jpg"
            await message.download_media(file=image_path)
            msg["image_path"] = str(image_path)

        messages_data.append(msg)

    # Save raw JSON
    output_file = output_dir / f"{channel_name}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(messages_data, f, ensure_ascii=False, indent=2)

    logger.info(f"Completed scrape for {channel_name}. Messages: {len(messages_data)}")


# --------------------------------------------------
# Main
# --------------------------------------------------
async def main():
    async with TelegramClient("telegram_session", API_ID, API_HASH) as client:
        for channel_name, channel_url in CHANNELS.items():
            try:
                await scrape_channel(client, channel_name, channel_url)
            except Exception as e:
                logger.error(f"Error scraping {channel_name}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
