# TruyenQQ Auto Check-in

Bot điểm danh TruyenQQ hằng ngày: tự dò tên miền mới, tự đăng nhập, gọi API điểm danh và gửi thông báo qua Telegram/Discord.

Thiết kế để chạy trên **server tại nhà** (IP dân dụng), vì IP của GitHub Actions bị Cloudflare chặn. Toàn bộ runtime nằm trong một thư mục dự án, không cài package hệ thống.

---

## Tính năng

- **Tự dò tên miền**: đọc `truyenqq.link` và alias `truyenqq.bio`, lấy domain mới từ link `/lich-su`, câu thông báo "tên miền mới nhất...", canonical/`og:url` và mọi URL chứa `truyenqq`.
- **Kiểm tra domain sống**: chỉ dùng domain trả HTTP 200 và có nội dung TruyenQQ.
- **Cache domain**: lưu domain tốt nhất vào `.domain`; nếu nguồn lỗi, dùng cache trước khi fallback.
- **Tự đăng nhập**: Playwright mở popup đăng nhập, điền email/password; hỗ trợ `TRUYENQQ_COOKIE` nếu có.
- **Điểm danh bằng API**: gọi `POST /coins` với `action=daily_checkin`, đọc JSON trả về (`streak`, `amount`, `balance`).
- **Thông báo**: Telegram và/hoặc Discord webhook.
- **Chạy cron**: mặc định 07:30 sáng giờ Việt Nam.
- **Cô lập**: Python venv, Chromium, cache và log đều nằm trong thư mục dự án.

---

## Cấu trúc

```text
truyenqq_auto_checkin/
├── main.py              # logic chính
├── run.sh               # entrypoint cho cron
├── requirements.txt     # playwright, requests, playwright-stealth
├── .env.example         # mẫu cấu hình
├── .env                 # credentials thật (không commit, chmod 600)
├── .domain              # cache domain (tự sinh, không commit)
├── .venv/               # Python venv (tự tạo, không commit)
├── .browsers/           # Chromium của Playwright (tự tải, không commit)
├── .cache/              # cache runtime (tự sinh, không commit)
└── logs/                # log theo ngày (tự sinh, không commit)
```

---

## Yêu cầu

- Linux (đã kiểm chứng trên Ubuntu 24.04) hoặc Windows.
- Python 3.10+ (server đang dùng 3.12).
- `git`, `cron`.
- Không cần Docker, không cần cài `python3-pip` toàn hệ thống.

---

## Cài đặt trên server Ubuntu

### 1. Clone code

```bash
git clone https://github.com/HIepNgoc2006/truyenqq_auto_checkin.git ~/truyenqq_auto_checkin
cd ~/truyenqq_auto_checkin
```

### 2. Tạo venv trong thư mục dự án

```bash
python3 -m venv .venv
```

Nếu báo thiếu `ensurepip` (Ubuntu không có `python3-venv`), dùng cách không cần `apt`:

```bash
python3 -m venv --without-pip .venv
curl -sS https://bootstrap.pypa.io/get-pip.py -o .get-pip.py
.venv/bin/python .get-pip.py
rm .get-pip.py
```

### 3. Cài dependency và Chromium

```bash
.venv/bin/pip install -r requirements.txt
PLAYWRIGHT_BROWSERS_PATH="$PWD/.browsers" .venv/bin/playwright install chromium
```

Chromium được tải vào `./.browsers`, không vào `~/.cache`.

### 4. Cấu hình credentials

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Nội dung:

```ini
TRUYENQQ_EMAIL=your_email
TRUYENQQ_PASSWORD=your_password

# Tùy chọn
TRUYENQQ_COOKIE=
DISCORD_WEBHOOK_URL=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

`TRUYENQQ_COOKIE` chỉ là phương án phụ; nếu cookie hết hạn, script vẫn cần email/password để đăng nhập lại.

### 5. Chạy thử

```bash
./run.sh
tail -n 30 logs/checkin-$(date +%F).log
```

Kết quả thành công có dạng:

```text
🔎 Nguồn https://truyenqq.link: https://truyenqqko.com, https://truyenqq.bio
🌐 Tên miền sử dụng hôm nay: https://truyenqqko.com
🔑 Tiến hành đăng nhập tự động bằng Email/Password...
Đang gọi API điểm danh...
📢 ✅ Đã điểm danh TruyenQQ thành công trên https://truyenqqko.com! +1 coin, chuỗi 1 ngày, số dư 63.
```

Nếu đã điểm danh trong ngày:

```text
📢 ℹ️ Chưa điểm danh được: ['Bạn đã điểm danh hôm nay rồi.']
```

Đây là kết quả bình thường, không phải lỗi.

### 6. Cài cron

```bash
crontab -e
```

Thêm dòng:

```cron
30 0 * * * /home/hiep/truyenqq_auto_checkin/run.sh
```

Server dùng timezone UTC nên `30 0 * * *` = **07:30 giờ Việt Nam**. Nếu server dùng timezone khác, đổi giờ cho phù hợp.

Kiểm tra:

```bash
crontab -l
```

---

## Cách hoạt động

1. `get_latest_domain()`:
   - GET `https://truyenqq.link` (retry 3 lần, timeout 20s).
   - Trích domain từ link `/lich-su`, câu "tên miền mới nhất... là `<domain>`", canonical/`og:url`, và mọi URL chứa `truyenqq`.
   - Kiểm tra từng domain: HTTP 200 + nội dung có `truyenqq`/`truyện`.
   - Lưu domain sống vào `.domain`; nếu nguồn lỗi, đọc `.domain`, rồi mới fallback `truyenqqko.com` / `truyenqq.bio`.
2. Playwright mở `<domain>/coins`, nếu thấy nút **Đăng nhập** thì điền form popup và submit.
3. Gọi API:

   ```http
   POST /coins
   Content-Type: application/x-www-form-urlencoded

   action=daily_checkin
   ```

4. Đọc JSON:

   ```json
   {"status":1,"data":{"streak":1,"reward_type":"coin","amount":1,"balance":63}}
   ```

5. Gửi thông báo Telegram/Discord nếu đã cấu hình.
6. Ghi log vào `logs/checkin-YYYY-MM-DD.log`.

`run.sh` dùng `flock` để tránh hai lần chạy chồng nhau, và đặt:

```bash
PLAYWRIGHT_BROWSERS_PATH="$PWD/.browsers"
XDG_CACHE_HOME="$PWD/.cache"
```

---

## Chạy trên Windows (tùy chọn)

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\playwright install chromium
copy .env.example .env
.venv\Scripts\python main.py
```

Có thể dùng Task Scheduler thay cho cron. Lưu ý đặt `PLAYWRIGHT_BROWSERS_PATH` trỏ vào `.browsers` nếu muốn giữ browser trong dự án.

---

## GitHub Actions (không khuyến nghị)

Workflow `.github/workflows/daily_checkin.yml` vẫn còn nhưng đã bị tắt (`disabled_manually`).

Lý do: IP của GitHub Actions bị Cloudflare trả về `Just a moment...`, nên login và điểm danh thất bại. Chỉ bật lại nếu dùng **self-hosted runner** có IP dân dụng.

---

## Xử lý sự cố

| Hiện tượng | Nguyên nhân / cách xử lý |
|---|---|
| `Just a moment...` | IP bị Cloudflare chặn. Chạy từ mạng nhà hoặc self-hosted runner. Không phải lỗi selector. |
| `API điểm danh trả về dữ liệu không hợp lệ` | Endpoint hoặc JSON đã đổi. Kiểm tra `coins.js` của TruyenQQ và cập nhật `main.py`. |
| `Bạn đã điểm danh hôm nay rồi.` | Bình thường, không cần chạy lại. |
| Không tìm thấy nút Đăng nhập | Giao diện đổi selector. Cập nhật `login_btn` trong `main.py`. |
| `Không kiểm tra được domain nào` | `truyenqq.link`, cache và fallback đều lỗi. Kiểm tra mạng, cập nhật `FALLBACK_DOMAINS`. |
| `Domain không phản hồi` | Domain ứng viên chết hoặc bị chặn; script sẽ thử domain tiếp theo. |
| `python3 -m venv` báo thiếu `ensurepip` | Dùng `--without-pip` + `get-pip.py` như hướng dẫn, không cần `apt install`. |
| Playwright báo thiếu browser | Chạy lại `PLAYWRIGHT_BROWSERS_PATH="$PWD/.browsers" .venv/bin/playwright install chromium`. |
| Cron không chạy | Kiểm tra `crontab -l`, quyền thực thi `run.sh`, timezone server và file log. |
| Cron chạy nhưng không có log mới | Kiểm tra `flock`/process còn treo, hoặc `.env` thiếu credentials. |

---

## Bảo mật

- `.env` chứa mật khẩu thật; quyền `600`, không commit.
- `.env.test` (nếu dùng để thử nghiệm) cũng đã được ignore và phải để quyền `600`.
- Không dùng mật khẩu tài khoản chính nếu không cần; nên dùng tài khoản phụ.
- Không commit `.domain`, `.venv`, `.browsers`, `.cache`, `logs`.
- Không gửi mật khẩu qua chat/log; script không in credentials.

---

## Giới hạn và lưu ý

- Mỗi ngày chỉ điểm danh được một lần; API trả `status: 0` nếu đã điểm danh.
- Tài khoản mới có thể bị chặn bình luận cho đến khi xác thực email hoặc đủ thời gian hoạt động.
- Tự động hóa có thể vi phạm điều khoản sử dụng của TruyenQQ; dùng tài khoản phụ và tự chịu rủi ro.
- Không nên spam bình luận để cày EXP: có thể bị khóa tài khoản và không chứng minh được tác dụng.
- Phần thưởng theo cấp độ của TruyenQQ hiện ghi "đang phát triển".

---

## Lệnh nhanh

```bash
# chạy tay
~/truyenqq_auto_checkin/run.sh

# xem log hôm nay
tail -f ~/truyenqq_auto_checkin/logs/checkin-$(date +%F).log

# kiểm tra cron
crontab -l

# kiểm tra domain đang dùng
cat ~/truyenqq_auto_checkin/.domain

# cập nhật code
cd ~/truyenqq_auto_checkin && git pull --ff-only
```
