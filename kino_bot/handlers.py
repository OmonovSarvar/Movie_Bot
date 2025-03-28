from aiogram import Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from database import is_admin, add_admin, remove_admin, save_video, get_video, delete_video
from keyboards import get_subscription_keyboard
from utils import check_subscription
from config import MAIN_ADMIN_ID

class AddVideoState:
    waiting_for_video = "waiting_for_video"
    waiting_for_code = "waiting_for_code"

def register_handlers(dp: Dispatcher):
    @dp.message(Command("add_admin"))   
    async def add_admin_command(message: types.Message):
        """Admin qo'shish"""
        if message.from_user.id != MAIN_ADMIN_ID:
            await message.answer("Faqat asosiy admin yangi admin qo'shishi mumkin.")
            return
        
        args = message.text.split()
        if len(args) < 2:
            await message.answer("Foydalanuvchini qo'shish uchun: /add_admin USER_ID")
            return
        
        try:
            new_admin_id = int(args[1])
            if add_admin(new_admin_id):
                await message.answer(f"Admin {new_admin_id} muvaffaqiyatli qo'shildi.")
            else:
                await message.answer("Admin qo'shishda xatolik yuz berdi.")
        except ValueError:
            await message.answer("Noto'g'ri format. Foydalanish: /add_admin USER_ID")
    
    @dp.message(Command("remove_admin"))   
    async def remove_admin_command(message: types.Message):
        """Admin o‘chirish"""
        if message.from_user.id != MAIN_ADMIN_ID:
            await message.answer("Faqat asosiy admin adminlarni o‘chira oladi.")
            return
        
        args = message.text.split()
        if len(args) < 2:
            await message.answer("Adminni o‘chirish uchun: /remove_admin USER_ID")
            return
        
        try:
            admin_id = int(args[1])
            if remove_admin(admin_id):
                await message.answer(f"Admin {admin_id} muvaffaqiyatli o‘chirildi.")
            else:
                await message.answer("Admin o‘chirishda xatolik yuz berdi yoki u admin emas.")
        except ValueError:
            await message.answer("Noto'g'ri format. Foydalanish: /remove_admin USER_ID")
    
    @dp.message(Command("search"))
    async def search_video_command(message: types.Message):
        """Video qidirish"""
        keyboard = get_subscription_keyboard()
        if await check_subscription(message.bot, message.from_user.id):
            args = message.text.split()
            if len(args) < 2:
                await message.answer("Iltimos, /search VIDEO_CODE formatida kiriting.")
                return
            
            video_code = args[1]
            video_file_id = get_video(video_code)
            
            if video_file_id:
                async with ChatActionSender.upload_video(bot=message.bot, chat_id=message.chat.id):
                    await message.answer_video(video_file_id, caption="Mana siz so'ragan video!")
            else:
                await message.answer("Kechirasiz, bunday kodga ega video topilmadi.")
        else:
            await message.answer("Botimizga xush kelibsiz!. Botdan foydalanish uchun kanalga obuna bo'ling:", reply_markup=keyboard)

    @dp.message(Command("add_video"))
    async def add_video_command(message: types.Message, state: FSMContext):
        """Video qo‘shish jarayonini boshlash"""
        if not is_admin(message.from_user.id):
            await message.answer("Siz admin emassiz!")
            return

        await state.set_state(AddVideoState.waiting_for_video)
        await message.answer("Iltimos, yuklamoqchi bo'lgan videongizni jo‘nating.")

    @dp.message(F.video, StateFilter(AddVideoState.waiting_for_video))
    async def receive_video(message: types.Message, state: FSMContext):
        """Video faylni qabul qilish"""
        video_id = message.video.file_id
        await state.update_data(video_id=video_id)
        await state.set_state(AddVideoState.waiting_for_code)
        await message.answer("Videoga mos keladigan kodni kiriting.")

    @dp.message(StateFilter(AddVideoState.waiting_for_code))
    async def receive_video_code(message: types.Message, state: FSMContext):
        """Video kodini qabul qilish va bazaga saqlash"""
        data = await state.get_data()
        video_id = data.get("video_id")
        video_code = message.text.strip()

        if save_video(video_code, video_id):
            await message.answer("Video muvaffaqiyatli saqlandi!")
        else:
            await message.answer("Xatolik yuz berdi, iltimos qayta urinib ko‘ring.")

        await state.clear()

    @dp.message(Command("delete_video"))
    async def delete_video_command(message: types.Message):
        """Videoni o‘chirish"""
        if not is_admin(message.from_user.id):
            await message.answer("Siz admin emassiz!")
            return

        args = message.text.split()
        if len(args) < 2:
            await message.answer("Iltimos, /delete_video VIDEO_CODE formatida kiriting.")
            return

        video_code = args[1]
        if delete_video(video_code):
            await message.answer(f"Video {video_code} kod bilan o‘chirildi.")
        else:
            await message.answer("Kechirasiz, bunday kodga ega video topilmadi.")

def register_start_handler(dp: Dispatcher):
    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        keyboard = get_subscription_keyboard()
        if await check_subscription(message.bot, message.from_user.id):     
            await message.answer("Botimizga xush kelibsiz!")
        else:
            await message.answer("Botimizga xush kelibsiz!. Botdan foydalanish uchun kanalga obuna bo'ling:", reply_markup=keyboard)
