import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram import Router, F

from database import get_data_from_database, get_data_from_object, get_klient_price, get_one_klient, get_klient_count, show_chenge, show_not_abons, show_select_date_chenge
import config
import funcs
from buttons import first_admin_menu




TOKEN = config.TOKEN
dp = Dispatcher()



@dp.message(CommandStart())
def command_start_handler(message: Message) -> None:
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
        return message.answer("Привет!", reply_markup=first_admin_menu)
    else:
        return message.answer(f"Тебя нет в списке, твой id {message.from_user.id}. Напиши Максу свой id и своё Имя, если хочешь вступить.")

@dp.message(F.text == "Дубли")
def send_duble(message: Message) -> None:
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
            data = get_data_from_database()
            text = ""
            for item in data:
                text += f"{item[0]}: {item[1]}\n"
            return message.reply(text)
    else:
        pass

@dp.message(F.text == "Клиенты exel")
async def send_clients(message: types.Message):
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
            get_klient_price()
            file = types.input_file.FSInputFile(f'{funcs.get_yesterday()}_klient_price.xls')

            await message.answer_document(document=file)
    else:
        pass

@dp.message(F.text == "Счётчик Сисем exel")
def send_counter(message: types.Message):
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
            get_klient_count()
            file = types.input_file.FSInputFile(f'{funcs.get_yesterday()}_klient_count.xls')
            return message.answer_document(document=file)
    else:
        pass

@dp.message(F.text == "NewObject")
def send_new_object(message: types.Message):
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
            show_chenge()
            file = types.input_file.FSInputFile(f'{funcs.get_yesterday()}_show_chenge_objects_to_day.xls')
            return message.answer_document(document=file)
    else:
        pass

@dp.message(Command("лишние"))
def command_outsiders(message: types.Message, command: CommandObject):
    if command.args is None:
        return message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
            show_not_abons(command.args.split(" ")[0])
            file = types.input_file.FSInputFile(f'{funcs.get_yesterday()}_difference.xls')
            return message.answer_document(document=file)
    else:
        pass



def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    return dp.start_polling(bot, timeout=500)


            
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
