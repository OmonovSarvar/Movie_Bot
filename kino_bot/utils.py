import logging
from aiogram import Bot
from aiogram.types import ChatMember
from config import CHANNELS

async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        for channel in CHANNELS:
            chat_id = f"@{channel}" if not channel.startswith("@") else channel  
            chat_member: ChatMember = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if chat_member.status not in ("member", "administrator", "creator"):
                return False  # Agar foydalanuvchi bitta kanalga ham obuna bo'lmagan bo'lsa, False qaytariladi
        return True  # Agar barcha kanallarga obuna bo‘lsa, True qaytariladi
    except Exception as e:
        logging.error(f"Obuna tekshirishda xatolik: {e}")
        return False
