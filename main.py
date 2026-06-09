import os
import sys
import time
import requests
import re
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

# Sửa lỗi in emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def send_notification(message):
    """Gửi thông báo qua Telegram hoặc Discord nếu được cấu hình"""
    print(f"📢 {message}")
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()

    # Gửi Telegram
    if telegram_token and telegram_chat_id:
        try:
            url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
            requests.post(url, json={"chat_id": telegram_chat_id, "text": message}, timeout=10)
        except Exception as e:
            print(f"⚠️ Lỗi gửi thông báo Telegram: {e}")

    # Gửi Discord
    if discord_webhook:
        try:
            requests.post(discord_webhook, json={"content": message}, timeout=10)
        except Exception as e:
            print(f"⚠️ Lỗi gửi thông báo Discord: {e}")


def get_latest_domain():
    try:
        # Trang truyenqq.link luôn trỏ về tên miền mới nhất
        res = requests.get("https://truyenqq.link", timeout=10)
        
        # Tìm các link có dạng https://truyenqqxxx.com/lich-su
        match = re.search(r'href="(https://truyenqq[^\/"]+)/lich-su"', res.text)
        if match:
            domain = match.group(1)
            return domain
    except Exception as e:
        print(f"⚠️ Lỗi khi tìm tên miền mới nhất: {e}")
    
    fallback = "https://truyenqqko.com"
    return fallback

def parse_cookie_string(cookie_string, url):
    cookies = []
    for item in cookie_string.split(';'):
        if '=' in item:
            name, value = item.strip().split('=', 1)
            cookies.append({
                "name": name,
                "value": value,
                "url": url
            })
    return cookies

def check_in():
    cookie_str = os.environ.get("TRUYENQQ_COOKIE", "").strip()
    email = os.environ.get("TRUYENQQ_EMAIL", "").strip()
    password = os.environ.get("TRUYENQQ_PASSWORD", "").strip()

    if not cookie_str and not (email and password):
        msg = "❌ Lỗi: Bạn phải cấu hình TRUYENQQ_COOKIE hoặc (TRUYENQQ_EMAIL và TRUYENQQ_PASSWORD) trong GitHub Secrets."
        send_notification(msg)
        sys.exit(1)

    latest_domain = get_latest_domain()
    print(f"🌐 Tên miền sử dụng hôm nay: {latest_domain}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        if cookie_str:
            cookies = parse_cookie_string(cookie_str, latest_domain)
            context.add_cookies(cookies)

        page = context.new_page()
        stealth_sync(page)

        try:
            page.goto(f"{latest_domain}/coins", timeout=60000)
            page.wait_for_load_state("domcontentloaded")

            # Xử lý đăng nhập tự động
            print(f"Tiêu đề trang: {page.title()}")
            if "Cloudflare" in page.title() or "Just a moment" in page.title():
                print("⚠️ CẢNH BÁO: Phát hiện Cloudflare chặn IP của GitHub Actions!")
            
            login_btn = page.locator("button:has-text('Đăng nhập'), button:has-text('Đăng Nhập'), .btn-login").first
            print("Đang tìm nút Đăng nhập...")
            
            if login_btn.count() > 0 and login_btn.is_visible():
                if email and password:
                    print("🔑 Tiến hành đăng nhập tự động bằng Email/Password...")
                    login_btn.click()
                    time.sleep(2)
                    
                    email_input = page.locator("#email_login")
                    password_input = page.locator("#password_login")
                    
                    email_input.fill(email)
                    password_input.fill(password)
                    
                    page.locator(".button_login").click()
                    time.sleep(5)
                    
                    page.goto(f"{latest_domain}/coins", timeout=60000)
                    page.wait_for_load_state("networkidle")
                else:
                    send_notification("❌ Đăng nhập thất bại: Chưa cấu hình Email và Mật khẩu (Cookie có thể đã hết hạn).")
                    sys.exit(1)

            # Tìm nút điểm danh
            checkin_button = page.locator("text=/Điểm danh/i")
            if checkin_button.count() > 0 and checkin_button.first.is_visible():
                checkin_button.first.click()
                time.sleep(5)
                send_notification(f"✅ Đã điểm danh TruyenQQ thành công trên {latest_domain}!")
            else:
                send_notification("⚠️ Không tìm thấy nút Điểm danh. (Có thể bạn đã điểm danh rồi hoặc web đổi giao diện).")

        except Exception as e:
            send_notification(f"❌ Lỗi trong quá trình chạy script: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    check_in()
