from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import HEADLESS, CHROMEDRIVER_PATH


def create_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    if CHROMEDRIVER_PATH:
        print(f"[Driver] 使用本機 ChromeDriver：{CHROMEDRIVER_PATH}")
        service = Service(executable_path=CHROMEDRIVER_PATH)
    else:
        service = Service(ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=options)
