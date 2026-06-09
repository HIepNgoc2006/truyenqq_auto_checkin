# TruyenQQ Auto Check-in Bot 🤖

Bot tự động điểm danh hàng ngày trên TruyenQQ sử dụng **Python**, **Playwright**, và **GitHub Actions**. Bot hoạt động 24/7 hoàn toàn miễn phí trên Cloud, tự động cập nhật tên miền mới nhất và không yêu cầu treo máy.

## ✨ Tính năng nổi bật
- **Chạy tự động ngầm 100%**: Sử dụng GitHub Actions để chạy bot mỗi ngày (mặc định vào 07:30 sáng).
- **Tự động dò tên miền mới**: Bot tự động quét và tìm tên miền TruyenQQ mới nhất đang hoạt động (ví dụ `truyenqqko.com`, v.v.).
- **Auto Login chống hết hạn Cookie**: Sử dụng Email và Mật khẩu để tự động giả lập người dùng đăng nhập, giải quyết triệt để vấn đề Cookie bị hết hạn hoặc reset.
- **Thông báo đa nền tảng**: Tự động báo cáo kết quả điểm danh qua Telegram hoặc Discord.

---

## 🚀 Hướng dẫn cài đặt cho người mới

Bạn không cần biết code, không cần cài đặt ứng dụng gì trên máy tính. Chỉ cần làm theo 2 bước sau:

### Bước 1: Fork Repository này về tài khoản của bạn
1. Đăng nhập vào tài khoản GitHub của bạn.
2. Nhìn lên góc trên cùng bên phải của trang web này, bấm vào nút **Fork**.
3. Bấm **Create fork** để copy toàn bộ mã nguồn này về tài khoản cá nhân của bạn.

### Bước 2: Thiết lập Tài khoản đăng nhập (Secrets)
Để bot biết cần điểm danh cho tài khoản nào, bạn cần cung cấp thông tin đăng nhập cho bot. GitHub sẽ mã hóa và giấu kín thông tin này, **ngay cả bạn cũng không thể xem lại được mật khẩu sau khi đã nhập**.

1. Vào trang Repository mà bạn vừa Fork về.
2. Bấm vào tab **Settings** (Cài đặt) trên menu ngang.
3. Ở cột menu bên trái, cuộn xuống phần **Security**, chọn **Secrets and variables** -> **Actions**.
4. Bấm nút màu xanh **New repository secret** để thêm 2 biến bắt buộc sau:
   - **Tên:** `TRUYENQQ_EMAIL` | **Giá trị:** *Email tài khoản TruyenQQ của bạn*
   - **Tên:** `TRUYENQQ_PASSWORD` | **Giá trị:** *Mật khẩu tài khoản TruyenQQ của bạn*

*(Nhớ nhập chính xác tên biến ghi hoa toàn bộ như trên nhé).*

### Bước 3: (Tùy chọn) Nhận thông báo điểm danh
Nếu bạn muốn bot gửi tin nhắn báo cáo kết quả mỗi ngày, hãy tạo thêm các Secret sau:

**Nếu dùng Discord:**
- **Tên:** `DISCORD_WEBHOOK_URL` | **Giá trị:** *Đường link Webhook của kênh Discord của bạn*

**Nếu dùng Telegram:**
- **Tên:** `TELEGRAM_BOT_TOKEN` | **Giá trị:** *Token con bot lấy từ @BotFather*
- **Tên:** `TELEGRAM_CHAT_ID` | **Giá trị:** *ID Telegram của bạn (Lấy từ @userinfobot)*

---

## 🛠️ Cách chạy thử Bot ngay lập tức
Mặc định bot sẽ tự động chạy vào lúc 07:30 sáng giờ VN. Để kiểm tra bot có hoạt động hay không ngay bây giờ:
1. Chuyển sang tab **Actions** trên Repository của bạn.
2. (Lần đầu tiên) Bấm nút xanh **"I understand my workflows, go ahead and enable them"**.
3. Ở cột bên trái, bấm vào **TruyenQQ Daily Check-in**.
4. Bấm nút xổ xuống **Run workflow** (ở bên phải) -> Bấm tiếp **Run workflow** màu xanh.
5. Chờ vài giây và tải lại trang, bấm vào luồng đang chạy để xem nhật ký (Log) điểm danh.

## ⚠️ Khuyến cáo bảo mật
- Mã nguồn này được cung cấp hoàn toàn mã nguồn mở, bạn có thể tự do kiểm tra mã nguồn tại file `main.py`. Mật khẩu của bạn không bị gửi cho bất kỳ ai ngoài máy chủ của TruyenQQ.
- Nếu không an tâm, bạn có thể đăng ký một tài khoản TruyenQQ phụ bằng Email rác để chạy thử.

---
*Phát triển bởi [Tên của bạn/HiepNgoc2006]*