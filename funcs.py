import datetime
import pandas as pd
import psycopg2
import Levenshtein



def get_yesterday() -> str:
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def get_monitoring_system(value: str) -> str:
    if value == "11" or value == 11:
        return "WHost"
    elif value == "12" or value == 12:
        return "Fort"
    elif value == "13" or value == 13:
        return "GSoft"
    elif value == "14" or value == 14:
        return "Scout"
    elif value == "15" or value == 15:
        return "Era"
    elif value == "16" or value == 16:
        return "WLocal"
    else:
        return ""

def count_objects(data):
    # Создаем словарь для хранения информации
    clients = {}

    # Проходимся по исходному массиву и заполняем словарь
    for client, system, obj in data:
        if client not in clients:
            clients[client] = {}
        if system not in clients[client]:
            clients[client][system] = 0
        clients[client][system] += 1

    # Формируем строку с нужным форматированием
    result = ""
    for client, systems in clients.items():
        for system, count in systems.items():
            result += f"{client}, {system}, {count}\n"

    return result

def klient_count(data):
    # Создаем словарь для хранения информации
    clients = {}

    # Проходимся по исходному массиву и заполняем словарь
    for client, system, obj in data:
        if client not in clients:
            clients[client] = {}
        if system not in clients[client]:
            clients[client][system] = 0
        clients[client][system] += 1

    # Формируем список кортежей с нужным форматированием
    result = []
    for client, systems in clients.items():
        for system, count in systems.items():
            result.append((client, system, count))

    return result

def check_excel_double():

    # Загрузка данных из файла Excel
    df = pd.read_excel(f'{get_yesterday()}_klient_price.xls')

    # Выбор столбца, в котором нужно найти дубликаты
    column_name = 'Объект'

    # Поиск дубликатов строк в столбце
    duplicates = df[df.duplicated(subset=column_name)]

    # Вывод найденных дубликатов
    return duplicates


