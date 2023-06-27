import datetime



def get_yesterday() -> str:
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def get_monitoring_system(value: str) -> str:
    if value == "11":
        return "WHost"
    elif value == "12":
        return "Fort"
    elif value == "13":
        return "GSoft"
    elif value == "14":
        return "Scout"
    elif value == "15":
        return "Era"
    elif value == "16":
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
