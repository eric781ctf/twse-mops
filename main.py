import time
from datetime import datetime, timedelta
from utils.daily_logger import DailyLogHandler
from services.retrieve_api import do_task

log_handler = DailyLogHandler(log_dir="logs")
logger = log_handler.get_logger()

def wait_until(hour, minute):
    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= target:
        # 如果今天的時間已經過了，就等明天的
        target += timedelta(days=1)
    delta = (target - now).total_seconds()
    logger.info(f"Waiting until {target.strftime('%Y-%m-%d %H:%M:%S')} ({delta:.0f}s)")
    time.sleep(delta)

while True:
    log_handler.check_and_rotate()  # 每次 loop 都檢查是否要換日
    logger.info("Still running...")
    DAY_AVG_MONTH_PATH, DAY_ALL_PATH = do_task()
    logger.info("每日任務完成，等待隔日執行")
    wait_until(8, 30)
