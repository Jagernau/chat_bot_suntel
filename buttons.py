from telebot.types import ReplyKeyboardMarkup, KeyboardButton

first_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
client_excel = KeyboardButton(text="Клиенты exel")
dubles = KeyboardButton(text="Дубли")
counter_excel = KeyboardButton(text="Счётчик Сисем exel")
new_object = KeyboardButton(text="NewObject")

first_admin_menu.add(client_excel, dubles, counter_excel, new_object)

