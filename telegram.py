import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from database import get_data_from_database, get_data_from_object, get_klient_price, get_one_klient, get_klient_count, show_chenge
import config
import funcs
from buttons import keyboard
from prettytable import PrettyTable
import re

API_TOKEN = config.TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
        await message.reply("Привет!", reply_markup=keyboard)
    else:
        await message.reply(f"Тебя нет в списке, твой id {message.from_user.id}. Напиши Максу свой id и своё Имя, если хочешь вступить.")


@dp.message_handler(content_types=["text"])
async def send_data(message: types.Message):
    if (
        str(message.from_user.id) in config.USERS_ID_LIST
    ):
        if message.text == "Дубли":
            data = await get_data_from_database()
            text = ""
            for item in data:
                text += f"{item[0]}: {item[1]}\n"
            await message.reply(text)

        if message.text == "Клиенты exel":
            get_klient_price()
            file = types.InputFile(f'{funcs.get_yesterday()}_klient_price.xls')
            await bot.send_document(chat_id=message.from_user.id, document=file)


        if  message.text != "Дубли" and message.text != "Клиенты exel" and message.text != "Счётчик Сисем exel":
            data_array = get_one_klient(message.text)
            if len(data_array) >= 1:
                await message.reply(funcs.count_objects(data_array))
            else:
                message.reply(f"{message.text} Такого клиента нет")


        if message.text != "Счётчик Сисем exel" and message.text != "Клиенты excel" and message.text != "Дубли":
            data = await get_data_from_object(message.text)

            text = ""
            for item in data:
                text += f"\n{item[0]}➡️{funcs.get_monitoring_system(str(item[2]))}➡️{item[3]}\n"
            if text == "":
                await message.reply(f"{message.text} не найден объект с таким именем")
            else:
                await message.reply(text)

        if message.text == "Счётчик Сисем exel":
            get_klient_count()
            file = types.InputFile(f'{funcs.get_yesterday()}_klient_count.xls')
            await bot.send_document(chat_id=message.from_user.id, document=file)

        if message.text == "Одинаковые имена объектов":
            double = funcs.check_excel_double()
            await message.reply(str(double))

        if "new: " in message.text:
            chenge = show_chenge(str(message.text).replace("new: ", ""))
            if chenge == None:
                await message.reply(f"{message.text} не найдены изменения за этот срок")
            else:
                file = types.InputFile(f'{funcs.get_yesterday()}_show_chenge_objects_to_day.xls')

                await bot.send_document(chat_id=message.from_user.id, document=file)


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
