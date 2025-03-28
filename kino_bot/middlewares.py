import logging
from aiogram import BaseMiddleware, Bot
from aiogram.types import ChatMember, Update, User
from typing import Callable, Awaitable, Dict, Any
from config import CHANNELS
from keyboards import get_subscription_keyboard

EVENT_FROM_USER = 'event_from_user'

class CheckSubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]], 
        event: Update, 
        data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data['bot']
        user: User = data.get(EVENT_FROM_USER)
        
        if not user:
            return await bot.send_message(chat_id=event.chat.id, text="Foydalanuvchi ma'lumoti yo'q.")
        
        # ❗ Foydalanuvchi barcha kanallarga obuna bo'lganmi?
        not_subscribed_channels = []

        for channel in CHANNELS:
            try:
                chat_member: ChatMember = await bot.get_chat_member(chat_id=channel, user_id=user.id)
                if chat_member.status not in ("member", "administrator", "creator"):
                    not_subscribed_channels.append(channel)
            except Exception as e:
                logging.error(f"❌ Xatolik: {e} | Kanal: {channel}")
        
        if not_subscribed_channels:
            return await bot.send_message(
                chat_id=user.id, 
                text="📢 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:",
                reply_markup=get_subscription_keyboard()
            )
        
        return await handler(event, data)
