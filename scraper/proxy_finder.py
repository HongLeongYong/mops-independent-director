import requests
from config import ENTRY_URL, PROXIES, PROXY_TEST_TIMEOUT


def find_working_proxy() -> dict | None:
    """逐一測試 PROXIES，回傳第一個可用的 proxy dict，全部失敗回傳 None。"""
    print(f"[Proxy] 開始測試 {len(PROXIES)} 個 proxy...")

    for i, proxy in enumerate(PROXIES, 1):
        addr = proxy.get("http") or proxy.get("https", "")
        print(f"[Proxy] 測試 {i}/{len(PROXIES)}：{addr}", end=" ... ", flush=True)
        try:
            resp = requests.get(
                ENTRY_URL,
                proxies=proxy,
                timeout=PROXY_TEST_TIMEOUT,
                verify=False,
            )
            if resp.status_code < 500:
                print("✓ 可用")
                return proxy
            else:
                print(f"✗ HTTP {resp.status_code}")
        except Exception as e:
            print(f"✗ {e}")

    print("[Proxy] 所有 proxy 均無法連線")
    return None
