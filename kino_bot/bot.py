import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
import os

from config import BOT_TOKEN
from database import create_db
from handlers import register_handlers, register_start_handler
from middlewares import CheckSubscriptionMiddleware

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def handle_request(request):
    try:
        update = await request.json()
        await dp.feed_webhook_update(bot, update)
        return web.Response(text="OK")
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        return web.Response(status=500, text="Xatolik yuz berdi")

def setup_middlewares():
    dp.update.middleware(CheckSubscriptionMiddleware())

async def on_startup():
    logging.info("Bot ishga tushmoqda...")
    create_db()
    setup_middlewares()
    register_handlers(dp)
    register_start_handler(dp)

    # Webhook URL
    WEBHOOK_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "https://movie-bot-i2lc.onrender.com")
    WEBHOOK_URL = f"https://{WEBHOOK_HOST}/webhook"

    logging.info(f"Webhook o‘rnatilmoqda: {WEBHOOK_URL}")
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown():
    logging.info("Webhook o‘chirilmoqda...")
    await bot.delete_webhook()

async def main():
    await on_startup()

    # Web server yaratish
    app = web.Application()
    app.router.add_post("/webhook", handle_request)

    # Port sozlash
    PORT = int(os.environ.get("PORT", 8080))

    logging.info(f"Server {PORT}-portda ishlamoqda...")
    return app, PORT

if __name__ == "__main__":
    app, port = asyncio.run(main())
    web.run_app(app, host="0.0.0.0", port=port)
