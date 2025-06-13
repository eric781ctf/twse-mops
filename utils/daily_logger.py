import logging
import os
import time
from datetime import datetime

class DailyLogHandler:
    def __init__(self, log_dir="./app/logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.logger = logging.getLogger("DailyLogger")
        self.logger.setLevel(logging.INFO)
        self._setup_handler()

    def _setup_handler(self):
        log_filename = f"{self.current_date}.log"
        log_path = os.path.join(self.log_dir, log_filename)

        # 移除舊 handler
        if self.logger.handlers:
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)
                handler.close()

        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(logging.StreamHandler())  # 同時印出到 console

    def check_and_rotate(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self.current_date:
            self.current_date = today
            self._setup_handler()

    def get_logger(self):
        return self.logger
