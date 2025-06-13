class APIConfig:
    BASE_URL = "https://openapi.twse.com.tw/v1/exchangeReport/"
    STOCK_DAY_AVG_MONTH = "STOCK_DAY_AVG_ALL" # 上市個股日收盤價及月平均價
    STOCK_DAY_ALL = "STOCK_DAY_ALL" # 上市個股日成交資訊
    BWIBBU_ALL = "BWIBBU_ALL" # 上市個股日本益比、殖利率及股價淨值比（依代碼查詢）

class StorageConfig:
    STORAGE_PATH = "app/storage/"
    LOGGING_PATH = "app/logs/"
    ANALYZE_PATH = "app/analyze/"