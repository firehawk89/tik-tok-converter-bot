import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MS_TOKEN = os.getenv("MS_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено у змінних середовища!")
