# AI Agent Rules & Instructions

## Git Workflow
Mọi AI assistant (Claude, Cursor, Copilot, Antigravity CLI...) khi làm việc trong project này phải tuân thủ nghiêm ngặt quy tắc sau:

1. **Auto-commit & Push**: Sau khi hoàn thành một yêu cầu của người dùng và có bất kỳ thay đổi nào về file (thêm, sửa, xóa), AI **PHẢI TỰ ĐỘNG** thực hiện các lệnh sau:
   - `git add .`
   - `git commit -m "<mô tả ngắn gọn gọn thay đổi>"`
   - `git push`

2. **Không cần chờ người dùng nhắc**: Quá trình này phải được thực thi tự động ở cuối mỗi chu trình xử lý mà không cần hỏi lại người dùng, trừ phi nội dung code đang chạy thử bị lỗi.
