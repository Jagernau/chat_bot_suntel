import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from database import get_data_from_database, get_data_from_object
import config

API_TOKEN = config.TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Здесь добавьте хендлеры и функции для работы с базой данных
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Все Клиенты с большой буквы: ГОЛОВАНОВ,\n а если надо узнать дубли- дубли ")


@dp.message_handler(content_types=["text"])
async def send_data(message: types.Message):
    if (
        str(message.from_user.id) in config.USERS_ID_LIST
        and message.from_user.first_name in config.USERS_NAME_LIST
    ):
        if message.text == "дубли":
            data = await get_data_from_database()
            text = ""
            for item in data:
                text += f"{item[0]}: {item[1]}\n"
            await message.reply(text)
        else:
            data = await get_data_from_object(message.text)
            text = " "
            for item in data:
                text += f"{item[0]} {item[1]} {item[2]} {item[3]} {item[4]}\n"
            await message.reply(text)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
