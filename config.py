ENTRY_URL = "https://mops.twse.com.tw/mops/#/web/t93sc01_1"

# text: 下拉選單實際顯示文字；sheet: Excel sheet 名稱
MARKET_TYPES = [
    {"text": "上市",   "sheet": "上市"},
    {"text": "上櫃",   "sheet": "上櫃"},
    {"text": "興櫃",   "sheet": "興櫃"},
    {"text": "公開發行", "sheet": "公開銀行"},
]

BASE_OUTPUT_DIR = "result"    # 根資料夾，可自訂路徑
LATEST_SUBDIR   = "最新檔案"
HISTORY_SUBDIR  = "歷史記錄檔案"
OUTPUT_BASENAME = "獨立董事彙總表"

SPA_LOAD_WAIT = 3   # 秒，等 SPA 初始化
WAIT_TIMEOUT = 30
