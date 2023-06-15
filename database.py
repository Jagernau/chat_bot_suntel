import psycopg2
import config
import query
import pandas as pd
from styleframe import StyleFrame
import funcs



conn = psycopg2.connect(
    host=config.DB_HOST,
    port="5432",
    database=config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASSWORD
)

async def get_data_from_database():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vdubles;")
    data = cursor.fetchall()
    return data

async def get_data_from_object(name: str):
    cursor = conn.cursor()
    cursor.execute(f"select * from tdata t2 where t2.dimport = '2023-05-17 01:40:00' and upper(t2.object) like '%%{name}%%'")
    data = cursor.fetchall()
    return data

#функция которая результат data сохраняет в xlsx
def get_klient_price():
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


def get_klient_graf():
    cursor = conn.cursor()
    cursor.execute(query.klient_price)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Контрагент', 'Система', 'Объект'])
    df['Количество'] = df.groupby('Контрагент')['Объект'].transform('count')
    df = df.sort_values(by='Контрагент')
    # в названии файла всавлять вчерашнее число
    excel_writer = StyleFrame.ExcelWriter(f'klient_counts.xls')
    sf = StyleFrame(df)
    sf.set_column_width('Контрагент', 30)
    sf.set_column_width('Система', 10)
    sf.set_column_width('Объект', 30)
    sf.to_excel(excel_writer=excel_writer)
    excel_writer.save()


