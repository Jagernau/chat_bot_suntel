import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from database import get_data_from_database
import config

API_TOKEN = config.TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Здесь добавьте хендлеры и функции для работы с базой данных
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я ваш чат-бот.")



@dp.message_handler(lambda message: message.text.lower() == 'данные')
async def send_data(message: types.Message):
    data = await get_data_from_database()
    text = ""
    for item in data:
        text += f"{item[0]}: {item[1]}\n"
    await message.reply(text)

@dp.message_handler(lambda message: message.text.lower() == 'данные')
async def send_data(message: types.Message):
    data = await get_data_from_database()
    text = ""
    for item in data:
        text += f"{item[0]}: {item[1]}\n"
    await message.reply(text)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
