import os
import re
import aiohttp
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

TIKTOK_REGEX = re.compile(r"(https?://(www\.)?tiktok\.com/[^\s]+)")

async def download_tiktok(url: str) -> bytes:
    api_url = f"https://api.kenkai.workers.dev/tiktok?url={url}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            if resp.status == 200:
                return await resp.read()
    return None

@dp.message(F.text)
async def handle_tiktok(message: Message):
    match = TIKTOK_REGEX.search(message.text)
    if match:
        video = await download_tiktok(match.group(1))
        if video:
            await bot.send_video(message.chat.id, video=video, caption="🎬 TikTok без водяного знаку")
            await message.delete()
        else:
            await message.reply("❌ Не вдалося завантажити відео")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
