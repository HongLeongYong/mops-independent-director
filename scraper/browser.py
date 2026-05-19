from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(headless: bool = True, proxy: dict | None = None) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    if proxy:
        # Chrome 只需一個 proxy 位址，優先取 https，否則取 http
        proxy_addr = proxy.get("https") or proxy.get("http")
        options.add_argument(f"--proxy-server={proxy_addr}")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)
