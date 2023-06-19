from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard = ReplyKeyboardMarkup(resize_keyboard=True )
keyboard.add(
    KeyboardButton(text="Клиенты"),
    KeyboardButton(text="Дубли"),
)


