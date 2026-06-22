from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List

# Khớp nối 100% với get_db từ core và hệ thống 17 bảng Models V2 thật
from app.core.database import get_db
from app.models.main_models import UserModel, DepartmentModel, KpiEventModel, KpiSummaryMonthlyModel
from app.api.auth import get_current_user  # Hàm bảo mật lấy thông tin Token giáo viên đang đăng nhập

router = APIRouter()

# ==============================================================================
# 📈 1. API ĐỒNG BỘ BIỂU ĐỒ ĐƯỜNG (KPI CÁC THÁNG CỦA CÁ NHÂN GIÁO VIÊN)
# ==============================================================================
@router.get("/my-monthly-kpi")
def get_my_monthly_kpi(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    current_year = datetime.now().year
    
    # 📌 Truy vấn bảng chuẩn kpi_summary_monthly của database_v2
    summaries = db.query(KpiSummaryMonthlyModel).filter(
        KpiSummaryMonthlyModel.user_id == current_user.user_id,
        KpiSummaryMonthlyModel.year == current_year
    ).order_by(KpiSummaryMonthlyModel.month.asc()).all()
    
    result = []
    # Nếu hệ thống chưa chạy tiến trình cron-job chốt sổ cuối tháng, tự động tính toán động tích lũy
    if not summaries:
        current_month = datetime.now().month
        for m in range(1, current_month + 1):
            end_of_month = datetime(current_year, m, 28)
            # Điểm thi đua quy chuẩn = 100đ nền + tổng (score_delta) biến động trong tháng
            total_delta = db.query(func.sum(KpiEventModel.score_delta)).filter(
                KpiEventModel.user_id == current_user.user_id,
                KpiEventModel.created_at <= end_of_month
            ).scalar() or 0
            
            result.append({
                "month": m,
                "score": float(100 + total_delta)
            })
        return result

    # Trả về mảng dữ liệu chuẩn khi đã có dữ liệu đóng băng cuối tháng
    return [{"month": s.month, "score": float(s.total_score)} for s in summaries]


# ==============================================================================
# 📊 2. API ĐỒNG BỘ BIỂU ĐỒ CỘT (KPI ĐIỂM TRUNG BÌNH THI ĐUA THEO KHỐI LỚP)
# ==============================================================================
@router.get("/departments-kpi")
def get_departments_kpi(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    # 📌 Lấy danh sách Khối lớp từ bảng departments chuẩn dựa theo school_id (Multi-School)
    departments = db.query(DepartmentModel).filter(
        DepartmentModel.school_id == current_user.school_id,
        DepartmentModel.is_active == True
    ).all()
    
    result = []
    for dept in departments:
        # Lấy tất cả user_id của giáo viên thuộc khối chuyên môn này
        teacher_ids = [u.user_id for u in db.query(UserModel).filter(
            UserModel.department_id == dept.department_id,
            UserModel.school_id == current_user.school_id
        ).all()]
        
        if not teacher_ids:
            result.append({"department_name": dept.department_name, "score": 100.0})
            continue
            
        # Tính tổng tất cả điểm thưởng/phạt thi đua của toàn bộ giáo viên trong khối
        total_delta = db.query(func.sum(KpiEventModel.score_delta)).filter(
            KpiEventModel.user_id.in_(teacher_ids)
        ).scalar() or 0
        
        # Điểm trung bình khối = (Số GV * 100đ nền + Tổng điểm biến động) / Tổng số GV trong khối
        avg_score = (len(teacher_ids) * 100 + total_delta) / len(teacher_ids)
        
        result.append({
            "department_name": dept.department_name,
            "score": round(avg_score, 1)
        })
        
    return result
