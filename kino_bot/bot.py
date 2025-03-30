import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from database import create_db
from handlers import register_handlers, register_start_handler
from middlewares import CheckSubscriptionMiddleware
import os

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=BOT_TOKEN)

def setup_middlewares():
    """Middlewarelarni o'rnatish"""
    dp.update.middleware(CheckSubscriptionMiddleware())

async def main():
    """Asosiy ishga tushirish funksiyasi"""
    logging.info("Bot ishga tushmoqda...")
    os.environ.get("PORT", 8080)
    create_db()  # Ma'lumotlar bazasini yaratish
    setup_middlewares()
    register_handlers(dp)# Handlerlarni ro‘yxatga olish
    register_start_handler(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
