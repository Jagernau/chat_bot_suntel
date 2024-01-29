from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

first_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,keyboard=[
    [
        KeyboardButton(text="Клиенты exel"),
        KeyboardButton(text="Дубли"),
    ],
    [
    KeyboardButton(text="Счётчик Сисем exel"),
    KeyboardButton(text="NewObject"),
    ],
]
)


