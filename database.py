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


