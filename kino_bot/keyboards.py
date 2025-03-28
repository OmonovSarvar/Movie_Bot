from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS

def get_subscription_keyboard():
    buttons = [] 
    for channel in CHANNELS:
        button = InlineKeyboardButton(text="Obuna bo'lish 📣", url=f"https://t.me/{channel}")
        buttons.append([button])  

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons) 
    return keyboard
