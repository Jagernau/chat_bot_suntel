import telebot

from database import get_data_from_database, get_data_from_object, get_klient_price, get_one_klient, get_klient_count, show_chenge, show_not_abons, show_select_date_chenge
import config
import funcs
from buttons import first_admin_menu




TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=["start"])
def command_start_handler(message: telebot.types.Message) -> None:
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
        bot.send_message(
                message.chat.id, 
                text=  "Привет!", 
                reply_markup=first_admin_menu
                )
    else:
        bot.send_message(message.chat.id, text=f"Тебя нет в списке, твой id {message.from_user.id}. Напиши Максу свой id и своё Имя, если хочешь вступить.")

@bot.message_handler(func=lambda message: message.text == "Дубли")
def send_duble(message: telebot.types.Message) -> None:
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
            data = get_data_from_database()
            text = ""
            for item in data:
                text += f"{item[0]}: {item[1]}\n"
            bot.send_message(message.chat.id, text=text)
    else:
        pass

@bot.message_handler(func=lambda message: message.text == "Клиенты exel")
def send_clients(message: telebot.types.Message):
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
            get_klient_price()
            file = telebot.types.InputFile(f'{funcs.get_yesterday()}_klient_price.xls')

            bot.send_document(message.chat.id, document=file)
    else:
        pass

@bot.message_handler(func=lambda message: message.text == "Счётчик Сисем exel")
def send_counter(message: telebot.types.Message):
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
            get_klient_count()
            file = telebot.types.InputFile(f'{funcs.get_yesterday()}_klient_count.xls')
            bot.send_document(message.chat.id, document=file)
    else:
        pass

@bot.message_handler(func=lambda message: message.text == "NewObject")
def send_new_object(message: telebot.types.Message):
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
            show_chenge()
            file = telebot.types.InputFile(f'{funcs.get_yesterday()}_show_chenge_objects_to_day.xls')
            bot.send_document(message.chat.id, document=file)
    else:
        pass

@bot.message_handler(commands=["лишние"])
def command_outsiders(message: telebot.types.Message, command: telebot.types.BotCommand) -> None:
    if command.to_dict().get("args") is None:
        bot.send_message(
            message.chat.id,

            "Ошибка: не переданы аргументы"
        )
        return
    if str(message.from_user.id) in list(config.USERS_ID_LIST):
            show_not_abons(str(command.to_dict().get("args")).split(" ")[0])
            file = telebot.types.InputFile(f'{funcs.get_yesterday()}_difference.xls')
            bot.send_document(message.chat.id, document=file)
    else:
        pass





if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()            
