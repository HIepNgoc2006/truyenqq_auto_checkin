import os
import sys
import time
import requests
import re
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

# Sửa lỗi in emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
FALLBACK_DOMAIN = "https://truyenqqko.com"
DOMAIN_SOURCE = "https://truyenqq.link"
DOMAIN_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".domain")

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


def _domain_alive(domain):
    """Kiểm tra domain còn phục vụ trang TruyenQQ thật hay không."""
    try:
        res = requests.get(domain, timeout=15, headers={"User-Agent": USER_AGENT})
        if res.status_code != 200:
            return False
        text = res.text.lower()
        return "truyenqq" in text or "truyện" in text
    except Exception:
        return False


def _extract_domains(html):
    """Lấy mọi domain có link /lich-su, ưu tiên domain chứa 'truyenqq'."""
    found = []
    for domain in re.findall(r'href="(https?://[^/"]+)/lich-su"', html):
        domain = domain.rstrip("/")
        if domain == DOMAIN_SOURCE or domain in found:
            continue
        found.append(domain)
    found.sort(key=lambda d: 0 if "truyenqq" in d.lower() else 1)
    return found


def _read_cached_domain():
    try:
        with open(DOMAIN_CACHE, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def _save_cached_domain(domain):
    try:
        with open(DOMAIN_CACHE, "w", encoding="utf-8") as f:
            f.write(domain + "\n")
    except OSError as e:
        print(f"⚠️ Không ghi được cache domain: {e}")


def get_latest_domain():
    headers = {"User-Agent": USER_AGENT}
    candidates = []

    # 1. Dò domain mới từ truyenqq.link, retry 3 lần
    for attempt in range(1, 4):
        try:
            res = requests.get(DOMAIN_SOURCE, timeout=20, headers=headers)
            if res.status_code == 200:
                candidates = _extract_domains(res.text)
                if candidates:
                    print(f"🔎 Domain ứng viên: {', '.join(candidates[:5])}")
                    break
            print(f"⚠️ Lần {attempt}: truyenqq.link trả HTTP {res.status_code}.")
        except Exception as e:
            print(f"⚠️ Lần {attempt}: không truy vấn được truyenqq.link ({e}).")
        if attempt < 3:
            time.sleep(2 * attempt)

    # 2. Chọn domain đầu tiên còn sống
    for domain in candidates[:5]:
        if _domain_alive(domain):
            _save_cached_domain(domain)
            return domain
        print(f"⚠️ Domain không phản hồi: {domain}")

    # 3. Dùng domain đã lưu từ lần chạy trước
    cached = _read_cached_domain()
    if cached and _domain_alive(cached):
        print(f"♻️ Dùng domain đã lưu: {cached}")
        return cached

    # 4. Fallback cuối cùng
    if _domain_alive(FALLBACK_DOMAIN):
        _save_cached_domain(FALLBACK_DOMAIN)
        return FALLBACK_DOMAIN

    print("⚠️ Không kiểm tra được domain nào, dùng fallback mặc định.")
    return FALLBACK_DOMAIN

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
        msg = "❌ Lỗi: Bạn phải cấu hình TRUYENQQ_COOKIE hoặc (TRUYENQQ_EMAIL và TRUYENQQ_PASSWORD) trong biến môi trường (file .env hoặc GitHub Secrets)."
        send_notification(msg)
        sys.exit(1)

    latest_domain = get_latest_domain()
    print(f"🌐 Tên miền sử dụng hôm nay: {latest_domain}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent=USER_AGENT
        )
        
        if cookie_str:
            cookies = parse_cookie_string(cookie_str, latest_domain)
            context.add_cookies(cookies)

        page = context.new_page()
        Stealth().apply_stealth_sync(page)

        try:
            page.goto(f"{latest_domain}/coins", timeout=60000)
            page.wait_for_load_state("domcontentloaded")

            # Xử lý đăng nhập tự động
            print(f"Tiêu đề trang: {page.title()}")
            if "Cloudflare" in page.title() or "Just a moment" in page.title():
                print("⚠️ CẢNH BÁO: Phát hiện Cloudflare chặn IP hiện tại!")
            
            login_btn = page.locator("button:has-text('Đăng nhập'), button:has-text('Đăng Nhập'), .btn-login, a:has-text('Đăng nhập'), a[title='Đăng nhập']").first
            print("Đang tìm nút Đăng nhập...")
            
            if login_btn.count() > 0 and login_btn.is_visible():
                if email and password:
                    print("🔑 Tiến hành đăng nhập tự động bằng Email/Password...")
                    login_btn.click()
                    
                    # Đợi form đăng nhập xuất hiện
                    email_input = page.locator("#email_login, input[type='email']").first
                    email_input.wait_for(state="visible", timeout=15000)
                    
                    password_input = page.locator("#password_login, input[type='password']").first
                    
                    email_input.fill(email)
                    password_input.fill(password)
                    
                    # Tìm và click nút submit đăng nhập
                    submit_btn = page.locator("#popup_content button.button_login, .popup-signin button.button_login").first
                    submit_btn.click()
                    time.sleep(5)
                    
                    page.goto(f"{latest_domain}/coins", timeout=60000)
                    page.wait_for_load_state("networkidle")
                else:
                    send_notification("❌ Đăng nhập thất bại: Chưa cấu hình Email và Mật khẩu (Cookie có thể đã hết hạn).")
                    sys.exit(1)

            # Gọi API điểm danh trực tiếp (coins.js dùng POST /coins với action=daily_checkin)
            print("Đang gọi API điểm danh...")
            resp = page.request.post(
                f"{latest_domain}/coins",
                form={"action": "daily_checkin"},
                headers={"Referer": f"{latest_domain}/coins"},
            )
            try:
                data = resp.json()
            except Exception:
                send_notification(f"❌ API điểm danh trả về dữ liệu không hợp lệ (HTTP {resp.status}).")
                sys.exit(1)

            if data.get("status") == 1:
                info = data.get("data") or {}
                send_notification(
                    f"✅ Đã điểm danh TruyenQQ thành công trên {latest_domain}! "
                    f"+{info.get('amount', '?')} {info.get('reward_type', 'coin')}, "
                    f"chuỗi {info.get('streak', '?')} ngày, số dư {info.get('balance', '?')}."
                )
            else:
                err = data.get("error") or data.get("message") or "không rõ lý do"
                send_notification(f"ℹ️ Chưa điểm danh được: {err}")

        except Exception as e:
            send_notification(f"❌ Lỗi trong quá trình chạy script: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    check_in()
