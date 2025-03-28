# import sqlite3
# import asyncio
# from typing import Callable, Awaitable, Dict, Any
# from aiogram import Bot, Dispatcher, types, F, BaseMiddleware
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from aiogram.types import Message, ChatMember, User, Update
# from aiogram.filters import Command
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.utils.chat_action import ChatActionSender
# import kino_bot.config as config
# import logging

# # Logging sozlamalari
# logging.basicConfig(level=logging.INFO)

# # Bot tokeni
# BOT_TOKEN = config.BOT_TOKEN

# # Admin ID
# MAIN_ADMIN_ID = 2128451813

# # Kanal ID (@ bilan)
# CHANNEL_ID = "@sarvaromon33"  

# # Bot va Dispatcher
# bot = Bot(token=BOT_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(storage=storage)

# # FSM uchun state
# class AddVideoState(StatesGroup):
#     waiting_for_video = State()
#     waiting_for_code = State()

# # Database funksiyalari
# def create_db():
#     """Ma'lumotlar bazasini yaratish"""
#     conn = sqlite3.connect("videos.db")
#     c = conn.cursor()
#     c.execute("""CREATE TABLE IF NOT EXISTS videos (
#                     video_code TEXT PRIMARY KEY,
#                     video_file_id TEXT NOT NULL
#                  )""")
#     c.execute("""CREATE TABLE IF NOT EXISTS admins (
#                     admin_id INTEGER PRIMARY KEY
#                  )""")
#     conn.commit()
#     conn.close()

# def is_admin(user_id):
#     """Foydalanuvchi admin ekanligini tekshirish"""
#     conn = sqlite3.connect("videos.db")
#     c = conn.cursor()
#     c.execute("SELECT * FROM admins WHERE admin_id = ?", (user_id,))
#     result = c.fetchone()
#     conn.close()
#     return result is not None or user_id == MAIN_ADMIN_ID

# def add_admin(user_id):
#     """Yangi admin qo'shish"""
#     try:
#         conn = sqlite3.connect("videos.db")
#         c = conn.cursor()
#         c.execute("INSERT OR IGNORE INTO admins (admin_id) VALUES (?)", (user_id,))
#         conn.commit()
#         conn.close()
#         return True
#     except Exception as e:
#         logging.error(f"Admin qo'shishda xatolik: {e}")
#         return False

# def save_video(video_code, video_file_id):
#     """Videoni ma'lumotlar bazasiga saqlash"""
#     try:
#         conn = sqlite3.connect("videos.db")
#         c = conn.cursor()
#         c.execute("INSERT OR REPLACE INTO videos (video_code, video_file_id) VALUES (?, ?)", 
#                   (video_code, video_file_id))
#         conn.commit()
#         conn.close()
#         return True
#     except Exception as e:
#         logging.error(f"Videoni saqlashda xatolik: {e}")
#         return False

# def get_video(video_code):
#     """Videoni kod bo'yicha topish"""
#     try:   
#         conn = sqlite3.connect("videos.db")
#         c = conn.cursor()
#         c.execute("SELECT video_file_id FROM videos WHERE video_code = ?", (video_code,))
#         result = c.fetchone()
#         conn.close()
#         return result[0] if result else None
#     except Exception as e:
#         logging.error(f"Videoni izlashda xatolik: {e}")
#         return None

# def delete_video(video_code):
#     """Videoni o'chirish"""
#     try:
#         conn = sqlite3.connect("videos.db")
#         c = conn.cursor()
#         c.execute("DELETE FROM videos WHERE video_code = ?", (video_code,))
#         rows_affected = c.rowcount
#         conn.commit()
#         conn.close()
#         return rows_affected > 0
#     except Exception as e:
#         logging.error(f"Videoni o'chirishda xatolik: {e}")
#         return False

# EVENT_FROM_USER = 'event_from_user'

# def inline_subscribe():
#     inline_keyboard = InlineKeyboardBuilder()

#     inline_keyboard.button(text='Subscribe', url='https://t.me/sarvaromon33')

#     return inline_keyboard.as_markup()

# class CheckSubscriptionMiddleware(BaseMiddleware):

#     async def __call__(
#             self,
#             handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
#             event: Update,
#             data: Dict[str, Any]
#     ) -> Any:
#         bot: Bot = data['bot']
#         user: User = data.get(EVENT_FROM_USER)

#         chat_member: ChatMember = await bot.get_chat_member(chat_id=config.SUBSCRIPTION_CHANNEL_ID, user_id=user.id)

#         if chat_member.status not in ("member", "administrator", "creator"):
#             return await bot.send_message(chat_id=user.id, text='Subscribe to group', reply_markup=inline_subscribe())

#         return await handler(event, data)


# __all__ = [
#     'CheckSubscriptionMiddleware'
# ]

# @dp.message(Command("add_admin"))   
# async def add_admin_command(message: Message):
#     """Admin qo'shish"""
#     if message.from_user.id != MAIN_ADMIN_ID:
#         await message.answer("Faqat asosiy admin yangi admin qo'shishi mumkin.")
#         return
    
#     try:
#         args = message.text.split()
#         if len(args) < 2:
#             await message.answer("Foydalanuvchini qo'shish uchun: /add_admin USER_ID")
#             return
            
#         new_admin_id = int(args[1])
#         if add_admin(new_admin_id):
#             await message.answer(f"Admin {new_admin_id} muvaffaqiyatli qo'shildi.")
#         else:
#             await message.answer("Admin qo'shishda xatolik yuz berdi.")
#     except (IndexError, ValueError):
#         await message.answer("Noto'g'ri format. Foydalanish: /add_admin USER_ID")

# @dp.message(Command("add_video"))
# async def add_video_command(message: Message, state: FSMContext):
#     """Video qo'shish jarayonini boshlash"""
#     if not is_admin(message.from_user.id):
#         await message.answer("Siz admin emassiz, video qo'sha olmaysiz.")
#         return
        
#     await message.answer("Iltimos, video yuboring.")
#     await state.set_state(AddVideoState.waiting_for_video)

# @dp.message(AddVideoState.waiting_for_video, F.video)
# async def receive_video(message: Message, state: FSMContext):
#     """Videoni qabul qilish"""
#     await state.update_data(video_file_id=message.video.file_id)
#     await message.answer("Video qabul qilindi! Endi unga kod kiriting.")
#     await state.set_state(AddVideoState.waiting_for_code)

# @dp.message(AddVideoState.waiting_for_code)
# async def receive_video_code(message: Message, state: FSMContext):
#     """Video uchun kodni qabul qilish"""
#     if not message.text:
#         await message.answer("Iltimos, matn formatida kod kiriting.")
#         return
        
#     data = await state.get_data()
#     video_file_id = data.get("video_file_id")
    
#     if not video_file_id:
#         await message.answer("Xatolik yuz berdi, iltimos qayta urinib ko'ring.")
#         await state.clear()
#         return
        
#     video_code = message.text.strip()
    
#     if save_video(video_code, video_file_id):
#         await message.answer(f"Video '{video_code}' kodi bilan muvaffaqiyatli saqlandi.")
#     else:
#         await message.answer("Videoni saqlashda xatolik yuz berdi.")
    
#     await state.clear()

# @dp.message(Command("search"))
# async def search_video_command(message: Message):
#     """Video qidirish"""
#     user_id = message.from_user.id
#     is_subscribed = await check_subscription(user_id)
    
#     if not is_subscribed:
#         await message.answer(
#             "Botdan foydalanish uchun quyidagi kanalga obuna bo'ling:", 
#             reply_markup=get_subscription_keyboard()
#         )
#         return
    
#     args = message.text.split()
#     if len(args) < 2:
#         await message.answer("Iltimos, /search VIDEO_CODE formatida kiriting.")
#         return
        
#     video_code = args[1]
#     video_file_id = get_video(video_code)
    
#     if video_file_id:
#         async with ChatActionSender.upload_video(bot=bot, chat_id=message.chat.id):
#             await message.answer_video(video_file_id, caption="Mana siz so'ragan video!")
#     else:
#         await message.answer("Kechirasiz, bunday kodga ega video topilmadi.")

# @dp.message(Command("delete"))
# async def delete_video_command(message: Message):
#     """Videoni o'chirish"""
#     if not is_admin(message.from_user.id):
#         await message.answer("Siz admin emassiz, video o'chira olmaysiz.")
#         return
        
#     args = message.text.split()
#     if len(args) < 2:
#         await message.answer("Iltimos, /delete VIDEO_CODE formatida foydalaning.")
#         return
        
#     video_code = args[1]
#     if delete_video(video_code):
#         await message.answer(f"Video '{video_code}' muvaffaqiyatli o'chirildi.")
#     else:
#         await message.answer(f"'{video_code}' kodli video topilmadi yoki o'chirishda xatolik yuz berdi.")

# @dp.message()
# async def all_messages(message: Message):
#     """Barcha boshqa xabarlar uchun handler"""
#     user_id = message.from_user.id
#     is_subscribed = await check_subscription(user_id)
    
#     if not is_subscribed:
#         await message.answer(
#             "Botdan foydalanish uchun quyidagi kanalga obuna bo'ling:", 
#             reply_markup=get_subscription_keyboard()
#         )
#         return
    
#     await message.answer("Video ko'rish uchun /search VIDEO_CODE buyrug'ini ishlating.")

# async def main():
#     """Asosiy funksiya"""
#     logging.info("Bot ishga tushmoqda...")
#     create_db()
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())