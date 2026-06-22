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

@app.post("/tasks/{task_id}/review/")
def review_task_and_generate_kpi(task_id: int, reviewer_id: int, actual_score: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhiệm vụ")
        
    now = datetime.now()
    is_late = now > task.deadline
    
    # ĐỒNG BỘ: Đổi sang từ khóa viết hoa của Flutter
    task.status = "COMPLETED" if not is_late else "OVERDUE"
    task.final_score = actual_score if not is_late else -task.score_value
    
    rule_code = "T_CM_01" if not is_late else "P_TD_01"
    rule = db.query(KpiRuleModel).filter(KpiRuleModel.rule_code == rule_code).first()
    
    if rule:
        kpi_event = KpiEventModel(
            user_id=task.assigned_to,
            rule_id=rule.rule_id,
            task_id=task.task_id,
            score_delta=task.final_score
        )
        db.add(kpi_event)
        
    db.add(AuditLogModel(actor_user_id=reviewer_id, action_type="REVIEW_TASK", description=f"Nghiệm thu việc '{task.title}' với số điểm thi đua thực đạt: {task.final_score}đ"))
    db.commit()
    return {"message": "Thành công"}

@app.get("/leaderboard/")
def get_leaderboard(db: Session = Depends(get_db)):
    teachers = db.query(UserModel).all()
    leaderboard = []
    
    for t in teachers:
        role = db.query(RoleModel).filter(RoleModel.role_id == t.role_id).first()
        dept = db.query(DepartmentModel).filter(DepartmentModel.department_id == t.department_id).first()
        
        if role and role.role_code in ["GIAO_VIEN", "TO_TRUONG"]:
            total_delta = db.query(func.sum(KpiEventModel.score_delta)).filter(KpiEventModel.user_id == t.user_id).scalar() or 0
            final_kpi = 100 + total_delta
            
            # ĐỒNG BỘ: Sửa 'DONE' -> 'COMPLETED', 'LATE' -> 'OVERDUE'
            done_count = db.query(TaskModel).filter(TaskModel.assigned_to == t.user_id, TaskModel.status == "COMPLETED").count()
            late_count = db.query(TaskModel).filter(TaskModel.assigned_to == t.user_id, TaskModel.status == "OVERDUE").count()
            
            leaderboard.append({
                "user_id": t.user_id,
                "full_name": t.full_name,
                "department": dept.department_name if dept else "Chưa phân tổ",
                "role": role.role_code,
                "total_score": final_kpi,
                "done_tasks": done_count,
                "late_tasks": late_count
            })
            
    leaderboard.sort(key=lambda x: x["total_score"], reverse=True)
    return leaderboard
    
@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "KPI School V2 Backend API của Trường TH Thạnh Xuân đang chạy mượt mà!",
        "note": "Cổng mạng nội bộ đã mở rộng hoàn toàn cho thiết bị di động."
    }