import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Lắng nghe request
    page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", lambda response: print("<<", response.status, response.url))
    
    page.goto("https://truyenqqko.com/coins")
    
    print("Clicking Đăng nhập...")
    # Thử click nút Đăng nhập
    page.locator("button:has-text('Đăng nhập')").first.click()
    
    time.sleep(5)
    
    # Thử tìm input email theo một cách chung chung hơn
    print(page.locator("input").count(), "inputs found on page")
    for i in range(page.locator("input").count()):
        el = page.locator("input").nth(i)
        print("Input:", el.get_attribute("name"), el.get_attribute("type"), el.get_attribute("id"))
        
    browser.close()
