from app.config import StorageConfig, APIConfig
from utils.util import get_yesterday
import os
import logging
import json
import requests
from datetime import datetime, timedelta



def request_and_download(api):
    logger = logging.getLogger("DailyLogger")
    logger.info("Function request_and_download() is running.")

    url = f"{APIConfig.BASE_URL}{api}"
    storage_data_date = get_yesterday()
    output_path = os.path.join(StorageConfig.STORAGE_PATH, f"{storage_data_date}_{api}.json")
    logger.debug(f"{api} output path: {output_path}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved {len(data)} data to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error：{e}")

def do_task():
    logger = logging.getLogger("DailyLogger")
    logger.info("Function do_task() is running.")

    DAY_AVG_MONTH_PATH = request_and_download(APIConfig.STOCK_DAY_AVG_MONTH)
    DAY_ALL_PATH = request_and_download(APIConfig.STOCK_DAY_ALL)
    return DAY_AVG_MONTH_PATH, DAY_ALL_PATH

