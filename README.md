# 獨立董事彙總表爬蟲

自動爬取台灣證券交易所 [公開資訊觀測站](https://mops.twse.com.tw/mops/#/web/t93sc01_1) 的獨立董事現職、經歷及兼任情形彙總表，支援上市、上櫃、興櫃、公開發行四種市場別，並自動與上一次爬蟲結果比對異動。

---

## 功能

- 爬取四個市場別（上市、上櫃、興櫃、公開銀行）的獨立董事兼任資料
- 合併輸出為單一 Excel 檔案，帶時間戳命名
- 自動與上一次結果比對，產出異動報告（新增 / 刪除 / 變更）
- 自動將異動人員與南山關係種類主檔比對，產出標註結果（疑似利害關係人 / 非利害關係人 / 非建檔範圍）
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
│   ├── compare.py            # 異動比對與清理
│   └── annotate.py           # 關係種類標註
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

### 4. 建立設定檔

複製範例設定檔，再依自己的環境修改：

```bash
cp config.example.py config.py
```

開啟 `config.py`，至少修改以下這行：

```python
BASE_OUTPUT_DIR = "/Users/username/Desktop/clawer_output"    # 改為自己的輸出路徑
```

如需啟用關係種類標註功能，填入關係種類 CSV 的完整路徑，並設定公司名稱：

```python
RELATION_FILE = "/Users/username/Desktop/關係種類.csv"
COMPANY_NAME  = "南山"   # 會帶入標註結果文字，例如「非南山利害關係人」
```

> 留空 (`""`) 時標註步驟會自動略過，不影響爬蟲與比對功能。

> `config.py` 已加入 `.gitignore`，不會被推上 GitHub，之後隨便改都沒關係。

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
6. 若有設定 `RELATION_FILE`，對比對結果執行關係種類標註，輸出 `annotated_compare_result_YYYYMMDD_HHMMSS.xlsx`
7. 清理 `最新檔案/`，只保留本次的兩份檔案

---

## 輸出檔案

### 爬蟲結果

檔名：`獨立董事彙總表_20260518_120000.xlsx`

| 欄位 | 說明 |
|------|------|
| 市場別 | 上市 / 上櫃 / 興櫃 / 公開銀行 |
| 序號 | 原始頁面序號 |
| 公司代號 | 股票代號 |
| 公司名稱 | 公司中文名稱 |
| 職稱 | 董事職稱 |
| 姓名 | 獨立董事姓名 |
| 就任日期 | 擔任獨立董事的就任日期 |
| 主要現職 | 目前主要職務 |
| 主要經歷 | 過去主要經歷 |
| 目前兼任其他公司董監事之情形-公司名稱 | 兼任公司名稱 |
| 目前兼任其他公司董監事之情形-職稱 | 兼任職稱 |
| 備註 | 備註欄位 |

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

### 標註結果

檔名：`annotated_compare_result_20260518_120000.xlsx`（需設定 `RELATION_FILE` 才會產出）

在比對結果的基礎上展開，每筆異動人員與關係種類主檔中的每一筆匹配紀錄對應一列。

| 欄位 | 說明 |
|------|------|
| （繼承比對結果所有欄位） | — |
| 姓名比對結果 | 非{COMPANY_NAME}利害關係人 / 與{COMPANY_NAME}利害關係人同名同姓 |
| 系統關係類別一 | 關係種類主檔 T 欄（關係類別）值 |
| 系統關係類別二 | 關係種類主檔 B 欄（關係類別）值，僅配偶條件成立時填入 |
| 比對結果 | 疑似為{COMPANY_NAME}利害關係人，需再進行確認 / 非建檔範圍 |
| 備註 | 空白欄位（供人工備註使用） |

---

## 注意事項

- 公開資訊觀測站為動態頁面（SPA），啟動時會等待頁面渲染，執行時間視網路狀況而定
- `歷史記錄檔案/` 不會自動清理，如需節省空間請手動管理
