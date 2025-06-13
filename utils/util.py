from datetime import datetime, timedelta
import os
import json

def get_yesterday():
    yesterday = datetime.today() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    return yesterday_str

def get_the_past_5_days():
    today = datetime.today()
    past_5_days = [today - timedelta(days=i) for i in range(1, 6)]
    return [date.strftime("%Y-%m-%d") for date in past_5_days]

def check_path(path):
    if os.path.exists(path):
        return True
    else:
        return False
    
def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)