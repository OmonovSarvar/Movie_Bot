import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from database import create_db
from handlers import register_handlers, register_start_handler
from middlewares import CheckSubscriptionMiddleware
from aiohttp import web
import os

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=BOT_TOKEN)

async def handle_request(request):
    """Telegram webhook ma'lumotlarini qabul qilish"""
    update = await request.json()
    await dp.feed_webhook_update(bot, update)
    return web.Response()

def setup_middlewares():
    """Middlewarelarni o'rnatish"""
    dp.update.middleware(CheckSubscriptionMiddleware())

async def main():
    logging.info("Bot ishga tushmoqda...")
    create_db()
    setup_middlewares()
    register_handlers(dp)
    register_start_handler(dp)

    # Webhook URL
    WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"

    # Webhook o‘rnatish
    await bot.set_webhook(WEBHOOK_URL)

    # Web serverni boshlash
    app = web.Application()
    app.router.add_post("/webhook", handle_request)

    PORT = int(os.environ.get("PORT", 8080))
    return app, PORT

if __name__ == "__main__":
    app, port = asyncio.run(main())
    web.run_app(app, host="0.0.0.0", port=port)
