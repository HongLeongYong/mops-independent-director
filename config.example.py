ENTRY_URL = "https://mops.twse.com.tw/mops/#/web/t93sc01_1"

# 瀏覽器設定
HEADLESS = True                # True：背景執行不跳出視窗；False：顯示瀏覽器視窗
CHROMEDRIVER_PATH = ""         # 留空則自動下載；填路徑則使用本機 chromedriver
# CHROMEDRIVER_PATH = "./chromedriver.exe"   # Windows 範例
# CHROMEDRIVER_PATH = "./chromedriver"       # macOS / Linux 範例

# text: 下拉選單實際顯示文字；sheet: Excel sheet 名稱
MARKET_TYPES = [
    {"text": "上市",   "sheet": "上市"},
    {"text": "上櫃",   "sheet": "上櫃"},
    {"text": "興櫃",   "sheet": "興櫃"},
    {"text": "公開發行", "sheet": "公開發行"},
]

BASE_OUTPUT_DIR = "/Users/username/Desktop/clawer_output"    # 修改為自己的輸出路徑
LATEST_SUBDIR   = "最新檔案"
HISTORY_SUBDIR  = "歷史記錄檔案"
OUTPUT_BASENAME = "獨立董事彙總表"
RELATION_FILE   = ""   # 關係種類 CSV 檔案的完整路徑，例如 "/Users/username/Desktop/關係種類.csv"
COMPANY_NAME    = "xx"             # 公司名稱，用於標註結果文字（例如 "鴻海"）

SPA_LOAD_WAIT = 3   # 秒，等 SPA 初始化
WAIT_TIMEOUT = 30

# 網路失敗重試設定
MAX_RETRIES = 3     # 每個市場別最多嘗試次數（含第一次）
RETRY_WAIT = 5      # 秒，重試前等待時間（每次遞增：5, 10, 15...）
