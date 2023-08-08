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
    port="5333",
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
    cursor.close()
    return data


async def get_data_from_object(name: str) -> typing.List:
    """
    Получение данных из базы данных по имени объекта
    Принимает имя объекта, отдвёт в виде списка

    """
    cursor = conn.cursor()
    cursor.execute(f"select * from tdata t2 where t2.dimport = (SELECT max(tdata.dimport) AS max FROM tdata) and (upper(t2.object) like '%%{name}%%' or t2.object like '%%{name}%%'or t2.object like upper('%%{name}%%'))")
    data = cursor.fetchall()
    cursor.close()
    return data


def get_klient_price() -> None:
    """
    Получение данных из базы данных
    сохраняет в xls таблицу клиентов, систеу мониторинга, объекты
    """
    cursor = conn.cursor()
    cursor.execute(query.klient_price)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Контрагент', 'Система', 'Объект'])
    excel_writer = StyleFrame.ExcelWriter(f'{funcs.get_yesterday()}_klient_price.xls')
    sf = StyleFrame(df)
    sf.set_column_width('Контрагент', 30)
    sf.set_column_width('Система', 10)
    sf.set_column_width('Объект', 30)

    sf.to_excel(excel_writer=excel_writer)
    excel_writer.save()
    cursor.close()

def get_one_klient(name: str):
    cursor = conn.cursor()
    cursor.execute(query.detail_klient.replace('XXX', name))
    data = cursor.fetchall()
    cursor.close()
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
    cursor.close()


def show_chenge():
    cursor = conn.cursor()
    cursor.execute(query.show_chenge_objects_to_day)
    today_data = cursor.fetchall()
    df = pd.DataFrame(today_data, columns=['Логин', 'Объект', 'Система'])
    df['Система'] = df['Система'].apply(lambda x: funcs.get_monitoring_system((x)))
    excel_writer = StyleFrame.ExcelWriter(f'{funcs.get_yesterday()}_show_chenge_objects_to_day.xls')
    sf = StyleFrame(df)
    sf.set_column_width('Логин', 30)
    sf.set_column_width('Объект', 40)
    sf.set_column_width('Система', 10)
    sf.to_excel(excel_writer=excel_writer)
    excel_writer.save()
    cursor.close()

def show_not_abons(id_system):
    cursor = conn.cursor()
    cursor.execute(query.all_db_object_today.replace('XXX', str(id_system)))
    today_objects = cursor.fetchall()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(query.abonents_object.replace('XXX', str(id_system)))
    abonents_objects = cursor.fetchall()
    cursor.close()

    set_today_objects = set()
    set_abonents_objects = set()

    for i in today_objects:
        set_today_objects.add(i[0])

    for i in abonents_objects:
        set_abonents_objects.add(i[1])

    difference = set_today_objects.difference(set_abonents_objects)
    idsystem = funcs.get_monitoring_system(id_system)
    df = pd.DataFrame(difference, columns=[str(idsystem)])
    excel_writer = StyleFrame.ExcelWriter(f'{funcs.get_yesterday()}_difference.xls')
    sf = StyleFrame(df)
    sf.set_column_width(str(idsystem), 50)
    sf.to_excel(excel_writer=excel_writer)
    excel_writer.save()
    

