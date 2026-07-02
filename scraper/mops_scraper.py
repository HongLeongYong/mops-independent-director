import time
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from config import ENTRY_URL, SPA_LOAD_WAIT, WAIT_TIMEOUT, MAX_RETRIES, RETRY_WAIT


def fetch_market_page(driver, market_text: str) -> str:
    """抓取單一市場別頁面，遇到網路/逾時錯誤自動重試。"""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return _fetch_market_page_once(driver, market_text)
        except (WebDriverException, TimeoutException) as e:
            last_error = e
            if attempt < MAX_RETRIES:
                wait_sec = RETRY_WAIT * attempt
                print(f"[重試] {market_text} 第 {attempt} 次失敗，{wait_sec} 秒後重試：{e}")
                time.sleep(wait_sec)
    # 重試耗盡，往外拋讓 main.py 記錄該市場別失敗
    raise last_error


def _fetch_market_page_once(driver, market_text: str) -> str:
    # 開新 tab，確保每次都是乾淨狀態
    driver.execute_script("window.open('');")
    new_tab = driver.window_handles[-1]
    for handle in driver.window_handles[:-1]:
        driver.switch_to.window(handle)
        driver.close()
    driver.switch_to.window(new_tab)

    driver.get(ENTRY_URL)
    time.sleep(SPA_LOAD_WAIT)  # 等 SPA 渲染完成

    # 找到含目標選項的 select，切換市場別
    selects = driver.find_elements(By.TAG_NAME, "select")
    for s in selects:
        options_text = [o.text for o in s.find_elements(By.TAG_NAME, "option")]
        if market_text in options_text:
            Select(s).select_by_visible_text(market_text)
            break

    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    original_handles = set(driver.window_handles)

    # 點擊查詢
    query_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='mainBtn' and contains(text(),'查詢')]"))
    )
    query_btn.click()

    # 等待結果新視窗出現並切換
    wait.until(lambda d: len(d.window_handles) > len(original_handles))
    result_handle = (set(driver.window_handles) - original_handles).pop()
    driver.switch_to.window(result_handle)

    # 等待表格載入
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

    return driver.page_source
