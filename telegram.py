import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from database import get_data_from_database, get_data_from_object, get_klient_price, get_one_klient
import config
import funcs
from buttons import keyboard
from prettytable import PrettyTable

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

        if message.text == "Клиенты":
            get_klient_price()
            file = types.InputFile(f'{funcs.get_yesterday()}_klient_price.xls')
            await bot.send_document(chat_id=message.from_user.id, document=file)

        if "Детально" in message.text:
            text = get_one_klient(message.text.replace("Детально ", ""))

            client_dict = {}
            objects_list = []
            for item in text:
                objects_list.append(item[2])
                client_dict[item[0]] = {item[1]: objects_list}

            
            await message.reply(f"{client_dict}")


        else:
            data = await get_data_from_object(message.text)

            text = " "
            for item in data:
                text += f"\n{item[0]}➡️{funcs.get_monitoring_system(str(item[2]))}➡️{item[3]}\n"
            await message.reply(text)


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
