import datetime
import os

def get_yesterday() -> str:
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

