import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


from config import BOT_TOKEN
from database import create_db
from handlers import register_handlers, register_start_handler
from middlewares import CheckSubscriptionMiddleware

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

def setup_middlewares():
    dp.update.middleware(CheckSubscriptionMiddleware())

async def on_startup():
    logging.info("Bot ishga tushmoqda...")
    create_db()
    setup_middlewares()
    register_handlers(dp)
    register_start_handler(dp)

async def main():
    await on_startup()
    logging.info("Polling boshlandi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to‘xtatildi.")
