#типизируй функции и задокументируй

import psycopg2
import config
import query
import pandas as pd
from styleframe import StyleFrame
import funcs
import typing


conn = psycopg2.connect(
    host=config.DB_HOST,
    port="5432",
    database=config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASSWORD
)

async def get_data_from_database() -> typing.List:
    """ 
    Получение данных из базы данных 
    Отдвёт в виде списка дублей

    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vdubles;")
    data = cursor.fetchall()
    return data


async def get_data_from_object(name: str) -> typing.List:
    """
    Получение данных из базы данных по имени объекта
    Принимает имя объекта, отдвёт в виде списка

    """
    cursor = conn.cursor()
    cursor.execute(f"select * from tdata t2 where t2.dimport = (SELECT max(tdata.dimport) AS max FROM tdata) and (upper(t2.object) like '%%{name}%%' or t2.object like '%%{name}%%'or t2.object like upper('%%{name}%%'))")
    data = cursor.fetchall()
    return data


def get_klient_price() -> None:
    """
    Получение данных из базы данных
    сохраняет в xls таблицу клиентов, систеу мониторинга, объекты
    """
    cursor = conn.cursor()
    cursor.execute(query.klient_price)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Контрагент', 'Система', 'Объект', 'Почта'])
    excel_writer = StyleFrame.ExcelWriter(f'{funcs.get_yesterday()}_klient_price.xls')
    sf = StyleFrame(df)
    sf.set_column_width('Контрагент', 30)
    sf.set_column_width('Система', 10)
    sf.set_column_width('Объект', 30)
    sf.set_column_width('Почта', 30)
    sf.to_excel(excel_writer=excel_writer)
    excel_writer.save()

def get_one_klient(name: str):
    cursor = conn.cursor()
    cursor.execute(query.detail_klient.replace('XXX', name))
    data = cursor.fetchall()
    return data

def get_klient_count():
    cursor = conn.cursor()
    cursor.execute(query.klient_price)
    data = cursor.fetchall()
    data_array = funcs.klient_count(data)
    df = pd.DataFrame(data_array, columns=['Контрагент', 'Система', 'Число объектов'])
    excel_writer = StyleFrame.ExcelWriter(f'{funcs.get_yesterday()}_klient_count.xls')
    sf = StyleFrame(df)
    sf.set_column_width('Контрагент', 30)
    sf.set_column_width('Система', 10)
    sf.set_column_width('Число объектов', 10)
    sf.to_excel(excel_writer=excel_writer)
    excel_writer.save()


