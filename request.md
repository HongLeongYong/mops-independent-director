# 我想要一個爬蟲程式

網頁
https://mops.twse.com.tw/mops/#/web/t93sc01_1

![alt text](image.png)

上市、上櫃、興櫃、公開銀行  的 獨立董事現職、經歷及兼任情形彙總表 我都要


以上市舉例

我先從 https://mops.twse.com.tw/mops/#/web/t93sc01_1 出發

在 市場別 中選擇 上市，然後 點擊 “查詢” 按鈕

之後會轉跳到另一個網頁

https://mopsov.twse.com.tw/mops/web/ajax_t93sc01_1?parameters=0eb65210d5bdc34ea16e295ccdbad1096c876e52264ebd5506826a4c5ced5ff215bb7c708f20bc1349cb0fefdb78bf513f6768abe5311d3c4cbd202639036e7c85e24402c4a1ea447b41c4651d815c9f


這裡的 parameters 應該是個隨機值

![alt text](image-1.png)
我需要把整個頁面的資料變成 一個 excel

欄位有很多，我全部欄位都要

把輸出結果放進資料夾 result 中

輸出結果 1 個 excel, 1個分頁，有欄位，市場別

輸出的 excel 請在後面加入 “_年月日_時間戳”
範例： 獨立董事彙總表_20260511_101500.xlsx

我想要和上一版 excel 做比對，然後產出一份 compare_result_20260511_101500.xlsx

需要比對的欄位
1. 市場別
2. 公司名稱
3. 姓名
4. 目前兼任其他公司董監事之情形-公司名稱
5. 目前兼任其他公司董監事之情形-職稱

爬完資料 → 產出 獨立董事彙總表_YYYYMMDD_HHMMSS.xlsx
自動在 result/ 找上一版檔案做比對
有異動就產出 compare_result_YYYYMMDD_HHMMSS.xlsx，包含欄位：

異動類型	市場別	公司名稱 姓名 公司代碼	舊_兼任公司名稱	舊_兼任職稱	新_兼任公司名稱	新_兼任職稱

公司代碼 不作為比較


# 新需求

在 config 中 設定一個 資料夾變數
如果資料夾變數下沒有 “最新檔案” 或者 “歷史記錄檔案” 就協助新增。
“最新檔案”  只留下 最新的  爬蟲結果 excel 和 比對結果 excel 
“歷史記錄檔案”  有的是 所有的 爬蟲結果 excel 和 比對結果 excel
每次執行爬蟲時，檔案都會同時寫入 “最新檔案” 和 “歷史記錄檔案” 。
執行比對時，都使用上一次留下來的 “最新檔案”  的 爬蟲結果 excel 。
如果  “最新檔案” 沒有 爬蟲結果 excel ，就不執行比對。
如果 “最新檔案”  裡面有多份 爬蟲結果 excel ，那請根據 excel命名排序。
執行完畢比對後，把上一次的 爬蟲結果 excel 和 比對結果 excel 刪除，只留下這一次的。

請幫我 寫 開發文檔，把程式的邏輯寫出來。
