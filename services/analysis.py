import os
import json
from utils.util import (
    get_yesterday, 
    get_the_past_5_days, 
    check_path,
    read_json
)
import logging
from app.config import StorageConfig, APIConfig

def check_storage_path(past_5_days_day_avg_month_path, past_5_days_day_all_path):
    logger = logging.getLogger("DailyLogger")
    logger.info("Function check_storage_path() is running.")
    for path in past_5_days_day_avg_month_path:
        if not check_path(path):
            logger.warning(f"Missing file: {path}")
            past_5_days_day_avg_month_path.remove(path)
    for path in past_5_days_day_all_path:
        if not check_path(path):
            logger.warning(f"Missing file: {path}")
            past_5_days_day_all_path.remove(path)
    return past_5_days_day_avg_month_path, past_5_days_day_all_path

def filter_day_higher_month(ListOfDict):
    data = {}
    for dictionary in ListOfDict:
        closed_price = dictionary.get("ClosingPrice")
        monthly_avg_price = dictionary.get("MonthlyAveragePrice")
        if closed_price > monthly_avg_price:
            data[dictionary["code"]] = []
            data[dictionary["code"]][dictionary["date"]] = {
                "Date": dictionary["Date"],
                "ClosingPrice": closed_price,
                "MonthlyAveragePrice": monthly_avg_price
            }
    return data

def mapping_avg_and_detail(target_data, DAL_yesterday_data):
    mapping_key = ["TradeVolume", "TradeValue", "OpeningPrice", "HighestPrice", "LowestPrice", "ClosingPrice", "Change", "Transaction"]
    for dictionary in DAL_yesterday_data:
        for key in mapping_key:
            target_data[dictionary["code"]][dictionary["date"]][key] = dictionary[key]
    return target_data




def analyze_data(DAY_AVG_MONTH_PATH, DAY_ALL_PATH):
    logger = logging.getLogger("DailyLogger")
    logger.info("Function analyze_data() is running.")
    yesterday = get_yesterday()
    past_5_days = get_the_past_5_days()

    # 在這裡添加你的數據分析邏輯
    logger.info(f"Yesterday: {yesterday}")
    logger.info(f"Past 5 Days: {past_5_days}")

    # 取得昨天的資料和前五天的資料路徑
    past_5_days_day_avg_month_path = [f"{StorageConfig.STORAGE_PATH}/{date}_STOCK_DAY_AVG_ALL.json" for date in past_5_days]
    past_5_days_day_all_path = [f"{StorageConfig.STORAGE_PATH}/{date}_STOCK_DAY_ALL.json" for date in past_5_days]
    past_n_days_day_avg_month_path, past_n_days_day_all_path = check_storage_path(past_5_days_day_avg_month_path, past_5_days_day_all_path)

    DAM_yesterday_data = read_json(DAY_AVG_MONTH_PATH)
    DAL_yesterday_data = read_json(DAY_ALL_PATH)

    target_data = filter_day_higher_month(DAM_yesterday_data)
    target_data = mapping_avg_and_detail(target_data, DAL_yesterday_data)

    with open(f'{StorageConfig.ANALYZE_PATH}/{yesterday}_ANALYZE.json', 'w') as f:
        json.dump(target_data, f, ensure_ascii=False, indent=4)