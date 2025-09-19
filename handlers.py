import logging
import re
from aiogram import F
from aiogram.types import Message
from download import download_tiktok

TIKTOK_REGEX = re.compile(r"(https?://(www\.)?(tiktok\.com|vm\.tiktok\.com)/[^\s]+)")

def register_handlers(dp, bot):
    @dp.message(F.text)
    async def handle_tiktok(message: Message):
        match = TIKTOK_REGEX.search(message.text)
        if not match:
            return

        tiktok_url = match.group(1)
        logging.info(f"Found TikTok URL: {tiktok_url}")

        video_data = await download_tiktok(tiktok_url)
        if video_data:
            await bot.send_video(
                chat_id=message.chat.id,
                video=video_data,
                caption="🎬 TikTok without watermark"
            )
            await message.delete()
            logging.info("Video sent, original message deleted")
        else:
            await message.reply("❌ Failed to download video")
            logging.warning("Sending video failed")
