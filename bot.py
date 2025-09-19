import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import handle_tiktok

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.message.register(handle_tiktok)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Webhook deleted (if it existed)")
    logging.info("Starting polling...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot crashed: {e}")

if __name__ == "__main__":
    logging.info("Bot is starting...")
    asyncio.run(main())
