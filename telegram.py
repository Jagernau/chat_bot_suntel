import telebot

from database import get_data_from_database, get_data_from_object, get_klient_price, get_one_klient, get_klient_count, show_chenge, show_not_abons, show_select_date_chenge
import config
import funcs
from buttons import first_admin_menu
from mail_sender import mails_sender
from my_logger import logger



TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN)


try:
    @bot.message_handler(commands=["start"])
    def command_start_handler(message: telebot.types.Message) -> None:
        if str(message.from_user.id) in list(config.USERS_ID_LIST):
            logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} отправил команду старт')
            bot.send_message(
                    message.chat.id, 
                    text=  "Привет!\nВсе excel файлы отправляются на почту.", 
                    reply_markup=first_admin_menu
                    )
        else:
            bot.send_message(message.chat.id, text=f"Тебя нет в списке, твой id {message.from_user.id}. Напиши Максу свой id и своё Имя, если хочешь вступить.")
            logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} попытался вступить в чат')
    logger.info('-----Блок start выполнен')
except Exception as e:
    logger.error(f'----Блок start возникла ошибка: {e}')


# @bot.message_handler(func=lambda message: message.text == "Дубли")
# def send_duble(message: telebot.types.Message) -> None:
#     if str(message.from_user.id) in list(config.USERS_ID_LIST):
#             data = get_data_from_database()
#             text = ""
#             for item in data:
#                 text += f"{item[0]}: {item[1]}\n"
#             bot.send_message(message.chat.id, text=text)
#     else:
#         pass

try:
    @bot.message_handler(func=lambda message: message.text == "Клиенты exel")
    def send_clients(message: telebot.types.Message):
        if str(message.from_user.id) in list(config.USERS_ID_LIST):
                logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} отправил команду klient_price')
                get_klient_price()
                file = f'{funcs.get_yesterday()}_klient_price.xls'
                mails_sender(str(message.from_user.id), file)
                bot.send_message(message.chat.id, text="Отправлено на почту")
        else:
            bot.send_message(message.chat.id, text="Тебя нет в списке, твой id {message.from_user.id}. Напиши Максу свой id и своё Имя, если хочешь вступить")
            logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} попытался запросить клиентов excel')

    logger.info('----Блок клиенты exel выполнен')
except Exception as e:
    logger.error(f'----Блок клиенты exel возникла ошибка: {e}')


try:
    @bot.message_handler(func=lambda message: message.text == "Счётчик Сисем exel")
    def send_counter(message: telebot.types.Message):
        if str(message.from_user.id) in list(config.USERS_ID_LIST):
                logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} отправил команду klient_count')
                get_klient_count()
                file = f'{funcs.get_yesterday()}_klient_count.xls'
                mails_sender(str(message.from_user.id), file)
                bot.send_message(message.chat.id, text="Отправлено на почту")
        else:
            bot.send_message(message.chat.id, text="Тебя нет в списке, твой id {message.from_user.id}. Напиши Максу свой id и своё Имя, если хочешь вступить")
            logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} попытался запросить счётчик систем')
            
    logger.info('----Блок счётчик Сисем exel выполнен')
except Exception as e:
    logger.error(f'----Блок счётчик Сисем возникла ошибка: {e}')



try:
    @bot.message_handler(func=lambda message: message.text == "NewObject")
    def send_new_object(message: telebot.types.Message):
        if str(message.from_user.id) in list(config.USERS_ID_LIST):
                logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} отправил команду new_object')
                show_chenge()
                file = f'{funcs.get_yesterday()}_show_chenge_objects_to_day.xls'
                
                mails_sender(str(message.from_user.id), file)
                bot.send_message(message.chat.id, text="Отправлено на почту")
        else:
            bot.send_message(message.chat.id, text="Тебя нет в списке, твой id {message.from_user.id}. Напиши Максу свой id и своё Имя, если хочешь вступить")
            logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} попытался запросить NewObject')

    logger.info('----Блок NewObject выполнен')
except Exception as e:
    logger.error(f'----Блок NewObject возникла ошибка: {e}')


try:
    @bot.message_handler(func=lambda message: message.text == "Команды инфо")
    def send_commands(message: telebot.types.Message) -> None:
        if str(message.from_user.id) in list(config.USERS_ID_LIST):
            logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} отправил команду команды инфо')
            bot.send_message(
                    message.chat.id, 
                    text="""
                    Команды:\n 
                    /start - Запуск бота\n
                    /лишние XXX - Список объектов не на абонентке\n
                        11 - Whost
                        12 - Fort
                        13 - Glonass
                        14 - Scout
                        15 - Era
                        16 - Wlocal
                    """
                    )
        else:
            bot.send_message(message.chat.id, text="Тебя нет в списке, твой id {message.from_user.id}. Напиши Максу свой id и своё Имя, если хочешь вступить")
        
            logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} попытался запросить список команд')

    logger.info('----Блок команды  инфо выполнен')
except Exception as e:
    logger.error(f'----Блок команды  инфо возникла ошибка: {e}')

try:
    @bot.message_handler(commands=["лишние"])
    def command_outsiders(message: telebot.types.Message) -> None:
        if str(message.from_user.id) in list(config.USERS_ID_LIST):
            args = str(message.text).split(" ")
            logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} отправил команду лишние {args}')
            if len(args) == 2:
                show_not_abons(args[1])
                file = f'{funcs.get_yesterday()}_difference.xls'
                mails_sender(str(message.from_user.id), file)
                bot.send_message(message.chat.id, text="Отправлено на почту")
                
            else:
                bot.send_message(message.chat.id, text="Неверное количество аргументов")
                
        else:
            bot.send_message(message.chat.id, text="Тебя нет в списке, твой id {message.from_user.id}. Напиши Максу свой id и своё Имя, если хочешь вступить")

            logger.info(f'Пользователь {message.from_user.id} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username} попытался запросить список команд')
    
    logger.info('----Блок команды  инфо выполнен')
except Exception as e:
    logger.error(f'----Блок команды  инфо возникла ошибка: {e}')




if __name__ == '__main__':
    logger.info('Бот запущен')
    bot.infinity_polling()            
