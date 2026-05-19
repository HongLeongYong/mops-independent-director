import os
from scraper.browser import create_driver
from scraper.mops_scraper import fetch_market_page
from scraper.proxy_finder import find_working_proxy
from parser.table_parser import parse_table
from exporter.excel_exporter import export_to_excel
from comparer.compare import find_previous_in_latest, run_compare
from config import MARKET_TYPES, BASE_OUTPUT_DIR, LATEST_SUBDIR, HISTORY_SUBDIR, USE_PROXY


def ensure_dirs():
    for subdir in [LATEST_SUBDIR, HISTORY_SUBDIR]:
        path = os.path.join(BASE_OUTPUT_DIR, subdir)
        os.makedirs(path, exist_ok=True)


def main():
    ensure_dirs()

    proxy = None
    if USE_PROXY:
        proxy = find_working_proxy()
        if proxy is None:
            print("[錯誤] 找不到可用的 proxy，程式終止")
            return

    # 爬蟲前先找舊版，避免寫入新檔後出現多份
    prev_file = find_previous_in_latest()

    all_data = {}
    driver = create_driver(proxy=proxy)
    try:
        for market in MARKET_TYPES:
            text = market["text"]
            sheet = market["sheet"]
            print(f"[開始] 爬取市場別：{text}")
            try:
                html = fetch_market_page(driver, text)
                records = parse_table(html)
                all_data[sheet] = records
                print(f"[完成] {text}：取得 {len(records)} 筆")
            except Exception as e:
                print(f"[錯誤] {text} 失敗：{e}")
                all_data[sheet] = []
    finally:
        driver.quit()

    new_file = export_to_excel(all_data)

    if new_file:
        run_compare(new_file, prev_file)


if __name__ == "__main__":
    main()
