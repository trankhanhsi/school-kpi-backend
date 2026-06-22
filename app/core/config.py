# ==========================================================
# 🔐 CẤU HÌNH JWT BẢO MẬT ĐỒNG BỘ CHO TRƯỜNG THẠNH XUÂN
# ==========================================================

# Khai báo cả 2 dạng tên biến để tất cả các file main.py và auth.py đều đọc chung một chìa khóa
SECRET_KEY = "Takeshi992002"
JWT_SECRET_KEY = "Takeshi992002"

# Thuật toán mã hóa Token JWT
ALGORITHM = "HS256"
JWT_ALGORITHM = "HS256"

# Thời gian hết hạn cấu hình
ACCESS_TOKEN_EXPIRE_HOURS = 8
REFRESH_TOKEN_EXPIRE_DAYS = 30

# 📡 CẤU HÌNH MỞ CỔNG CORS NỘI BỘ (BẮT BUỘC ĐỂ ĐIỆN THOẠI KẾT NỐI ĐƯỢC)
# Cho phép điện thoại truyền nhận gói tin mã hóa qua mạng Wi-Fi nội bộ
BACKEND_CORS_ORIGINS = ["*"]