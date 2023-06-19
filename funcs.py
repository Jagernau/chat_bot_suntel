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
