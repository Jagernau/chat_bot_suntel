from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard = ReplyKeyboardMarkup(resize_keyboard=True )
keyboard.add(
    KeyboardButton(text="Клиенты exel"),
    KeyboardButton(text="Дубли"),
    KeyboardButton(text="Счётчик Сисем exel"),
)


