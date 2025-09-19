import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MS_TOKEN = os.getenv("MS_TOKEN")
TIKTOK_BROWSER = os.getenv("TIKTOK_BROWSER", "chromium")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено у змінних середовища!")
