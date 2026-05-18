# 獨立董事彙總表爬蟲

自動爬取台灣證券交易所 [公開資訊觀測站](https://mops.twse.com.tw/mops/#/web/t93sc01_1) 的獨立董事現職、經歷及兼任情形彙總表，支援上市、上櫃、興櫃、公開發行四種市場別，並自動與上一次爬蟲結果比對異動。

---

## 功能

- 爬取四個市場別（上市、上櫃、興櫃、公開銀行）的獨立董事兼任資料
- 合併輸出為單一 Excel 檔案，帶時間戳命名
- 自動與上一次結果比對，產出異動報告（新增 / 刪除 / 變更）
- 雙資料夾管理：「最新檔案」只保留本次結果，「歷史記錄檔案」保留所有歷次結果
- 爬蟲背景執行，不跳出瀏覽器視窗

---

## 專案結構

```
.
├── main.py                   # 程式入口
├── config.py                 # 設定檔
├── scraper/
│   ├── browser.py            # Selenium 瀏覽器初始化
│   └── mops_scraper.py       # 頁面操作與資料擷取
├── parser/
│   └── table_parser.py       # HTML 表格解析
├── exporter/
│   └── excel_exporter.py     # Excel 輸出
├── comparer/
│   └── compare.py            # 異動比對與清理
└── result/
    ├── 最新檔案/              # 僅保留最新一次的爬蟲與比對結果
    └── 歷史記錄檔案/          # 保留所有歷次結果（不自動刪除）
```

---

## 環境需求

- Python 3.11+
- Google Chrome（需已安裝）

---

## 如何使用

### 1. 取得專案

**方法一：下載 ZIP（不需安裝 Git）**

至 [GitHub 頁面](https://github.com/HongLeongYong/mops-independent-director) 點擊 **Code → Download ZIP**，解壓縮後進入資料夾。

**方法二：Git Clone**

```bash
git clone https://github.com/HongLeongYong/mops-independent-director.git
cd mops-independent-director
```

### 2. 建立虛擬環境（建議）

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. 安裝套件

```bash
pip install -r requirements.txt
```

`webdriver-manager` 會自動下載對應版本的 ChromeDriver，無需手動安裝。

### 4. 調整設定（選用）

編輯 `config.py`，如需更改輸出根目錄或子資料夾名稱：

```python
BASE_OUTPUT_DIR = "result"    # 預設輸出到專案內的 result/，可改為絕對路徑
                               # 例如："/Users/yourname/Documents/output"
LATEST_SUBDIR   = "最新檔案"
HISTORY_SUBDIR  = "歷史記錄檔案"
```

子資料夾首次執行時會自動建立，無需手動新增。

### 5. 執行

```bash
python main.py
```

爬蟲在背景靜默執行，不會跳出瀏覽器視窗。執行完成後，結果會存放於 `result/最新檔案/`。

---

## 執行流程

1. 自動建立 `最新檔案/` 和 `歷史記錄檔案/` 資料夾（若不存在）
2. 讀取 `最新檔案/` 裡的上一次爬蟲結果（作為比對基準）
3. 爬取四個市場別資料
4. 輸出 `獨立董事彙總表_YYYYMMDD_HHMMSS.xlsx`，同時寫入兩個資料夾
5. 若有上一次結果，執行比對並輸出 `compare_result_YYYYMMDD_HHMMSS.xlsx`
6. 清理 `最新檔案/`，只保留本次的兩份檔案

---

## 輸出檔案

### 爬蟲結果

檔名：`獨立董事彙總表_20260518_120000.xlsx`

| 欄位 | 說明 |
|------|------|
| 市場別 | 上市 / 上櫃 / 興櫃 / 公開銀行 |
| 公司代號 | 股票代號 |
| 公司名稱 | 公司中文名稱 |
| 姓名 | 獨立董事姓名 |
| 目前兼任其他公司董監事之情形-公司名稱 | 兼任公司名稱 |
| 目前兼任其他公司董監事之情形-職稱 | 兼任職稱 |
| （其餘欄位） | 依原始頁面欄位全數保留 |

### 比對結果

檔名：`compare_result_20260518_120000.xlsx`

| 欄位 | 說明 |
|------|------|
| 異動類型 | 新增 / 刪除 / 變更 |
| 市場別 | — |
| 公司名稱 | — |
| 姓名 | — |
| 公司代號 | 不參與比對，僅帶入供參考 |
| 舊_目前兼任其他公司董監事之情形-公司名稱 | 舊值 |
| 舊_目前兼任其他公司董監事之情形-職稱 | 舊值 |
| 新_目前兼任其他公司董監事之情形-公司名稱 | 新值 |
| 新_目前兼任其他公司董監事之情形-職稱 | 新值 |

> 比對以「市場別 + 公司名稱 + 姓名」為 key，兼任公司名稱與職稱有任何變動即列為異動。

---

## 注意事項

- 公開資訊觀測站為動態頁面（SPA），啟動時會等待頁面渲染，執行時間視網路狀況而定
- `歷史記錄檔案/` 不會自動清理，如需節省空間請手動管理
