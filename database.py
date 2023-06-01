import psycopg2
import config
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
