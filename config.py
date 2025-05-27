import os
from dotenv import load_dotenv

load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_API_KEY")
GPT_BOT_TOKEN = os.getenv("GPT_TOKEN")

if not all([TG_BOT_TOKEN, GPT_BOT_TOKEN]):
    raise ValueError("Добавьте токены в .env")
