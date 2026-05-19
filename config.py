ENTRY_URL = "https://mops.twse.com.tw/mops/#/web/t93sc01_1"

# Proxy 設定
USE_PROXY = False
PROXIES = [
    {"http": "http://10.63.122.61:8080", "https": "http://10.63.122.61:8080"},
    # 在此填入其餘 proxy，格式相同
    # {"http": "http://10.x.x.x:8080", "https": "http://10.x.x.x:8080"},
]
PROXY_TEST_TIMEOUT = 10  # 每個 proxy 測試的 timeout（秒）

# text: 下拉選單實際顯示文字；sheet: Excel sheet 名稱
MARKET_TYPES = [
    {"text": "上市",   "sheet": "上市"},
    {"text": "上櫃",   "sheet": "上櫃"},
    {"text": "興櫃",   "sheet": "興櫃"},
    {"text": "公開發行", "sheet": "公開銀行"},
]

BASE_OUTPUT_DIR = "/Users/username/Desktop/clawer_output"    # 根資料夾，可自訂路徑
LATEST_SUBDIR   = "最新檔案"
HISTORY_SUBDIR  = "歷史記錄檔案"
OUTPUT_BASENAME = "獨立董事彙總表"

SPA_LOAD_WAIT = 3   # 秒，等 SPA 初始化
WAIT_TIMEOUT = 30
