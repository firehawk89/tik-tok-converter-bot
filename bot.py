import os
import re
import aiohttp
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logging.info("Loading environment variables...")

load_dotenv() 
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logging.error("BOT_TOKEN не знайдено в environment variables!")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

TIKTOK_REGEX = re.compile(r"(https?://(www\.)?tiktok\.com/[^\s]+)")

async def download_tiktok(url: str) -> bytes | None:
    api_url = f"https://api.kenkai.workers.dev/tiktok?url={url}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    logging.info(f"Downloaded video from {url}")
                    return await resp.read()
                else:
                    logging.warning(f"Failed to download video, status: {resp.status}")
    except Exception as e:
        logging.error(f"Exception while downloading video: {e}")
    return None

@dp.message(F.text)
async def handle_tiktok(message: Message):
    match = TIKTOK_REGEX.search(message.text)
    if not match:
        return  # не TikTok посилання

    tiktok_url = match.group(1)
    logging.info(f"Found TikTok URL: {tiktok_url}")

    video_data = await download_tiktok(tiktok_url)
    if video_data:
        await bot.send_video(
            chat_id=message.chat.id,
            video=video_data,
            caption="🎬 TikTok без водяного знаку"
        )
        await message.delete()
        logging.info("Video sent and original message deleted")
    else:
        await message.reply("❌ Не вдалося завантажити відео")
        logging.warning("Failed to send video")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Webhook deleted (if any existed)")

    logging.info("Starting bot polling...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot crashed: {e}")

if __name__ == "__main__":
    logging.info("Bot is starting...")
    asyncio.run(main())
