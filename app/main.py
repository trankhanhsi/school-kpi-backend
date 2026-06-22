from fastapi import FastAPI
import app.models  
from app.api import auth, task, evidence, report, notification
from fastapi.middleware.cors import CORSMiddleware

# 🏫 Khởi tạo máy chủ kết toán thi đua Trường TH Thạnh Xuân
app = FastAPI(
    title="Hệ thống quản lý thi đua Trường TH Thạnh Xuân",
    description="Backend API hỗ trợ đồng bộ dữ liệu đa nền tảng PC và Mobile",
    version="2.0.0"
)

# ==============================================================================
# 📡 CẤU HÌNH CORS ĐA THIẾT BỊ (MỞ RỘNG CỔNG CHO IPHONE / ANDROID QUA WI-FI)
# ==============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🌟 Cho phép cả trình duyệt PC và mạng mạng di động kết nối
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép đầy đủ các phương thức POST, GET, PUT, DELETE
    allow_headers=["*"],  # Cho phép truyền Header chứa mã Token bảo mật JWT
)

# ==============================================================================
# 🔀 ĐĂNG KÝ CÁC TUYẾN ĐƯỜNG DẪN ĐỊNH TUYẾN HỆ THỐNG (ROUTING)
# ==============================================================================
# 🔐 Đường dẫn gốc đăng nhập sẽ là: /auth/login/ (Thầy lưu ý để cấu hình vào Flutter)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
app.include_router(evidence.router, prefix="/evidences", tags=["Evidences"])
app.include_router(report.router, prefix="/reports", tags=["Reports"]) 
app.include_router(notification.router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "KPI School V2 Backend API của Trường TH Thạnh Xuân đang chạy mượt mà!",
        "note": "Cổng mạng nội bộ đã mở rộng hoàn toàn cho thiết bị di động."
    }
