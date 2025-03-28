import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
REDIS_URL = os.getenv("REDIS_URL")
DB_DNS = os.getenv("DB_DNS")
CHANNELS = ["sarvaromon_33", "evanovix"]
DB_NAME = "videos.db"
MAIN_ADMIN_ID = 2128451813
