from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List

from app.core.database import get_db
from app.models.main_models import UserModel, DepartmentModel, KpiEventModel, KpiSummaryMonthlyModel
from app.api.auth import get_current_user  # Thầy đảm bảo hàm này trả về User đang đăng nhập

router = APIRouter()

# ==============================================================================
# 📈 API 1: LẤY DỮ LIỆU ĐỘNG CHO BIỂU ĐỒ ĐƯỜNG (KPI CÁC THÁNG CỦA CÁ NHÂN)
# ==============================================================================
@router.get("/my-monthly-kpi")
def get_my_monthly_kpi(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    # Lấy năm hiện tại để lọc dữ liệu
    current_year = datetime.now().year
    
    # Truy vấn bảng kpi_summary_monthly để lấy điểm chốt các tháng của giáo viên
    summaries = db.query(KpiSummaryMonthlyModel).filter(
        KpiSummaryMonthlyModel.user_id == current_user.user_id,
        KpiSummaryMonthlyModel.year == current_year
    ).order_by(KpiSummaryMonthlyModel.month.asc()).all()
    
    # Nếu chưa có dữ liệu tổng hợp đóng băng cuối tháng, hệ thống tự động tính toán động
    # theo thời gian thực từ bảng kpi_events (Điểm nền 100 + Tổng delta tích lũy)
    result = []
    if not summaries:
        # Tạo mảng từ Tháng 1 đến Tháng hiện tại
        current_month = datetime.now().month
        for m in range(1, current_month + 1):
            # Tính tổng score_delta từ đầu năm đến hết tháng m đó
            end_of_month = datetime(current_year, m, 28) # Ước lượng cuối tháng
            total_delta = db.query(func.sum(KpiEventModel.score_delta)).filter(
                KpiEventModel.user_id == current_user.user_id,
                KpiEventModel.created_at <= end_of_month
            ).scalar() or 0
            
            result.append({
                "month": m,
                "score": float(100 + total_delta) # Điểm quy chuẩn nền 100
            })
        return result

    # Nếu đã có dữ liệu đóng băng thì trả về dữ liệu chuẩn
    return [{"month": s.month, "score": float(s.total_score)} for s in summaries]


# ==============================================================================
# 📊 API 2: LẤY DỮ LIỆU ĐỘNG CHO BIỂU ĐỒ CỘT (ĐIỂM TRUNG BÌNH THI ĐUA THEO KHỐI)
# ==============================================================================
@router.get("/departments-kpi")
def get_departments_kpi(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    # Lấy danh sách tất cả các khối phòng ban của trường học hiện tại (Multi-School)
    departments = db.query(DepartmentModel).filter(
        DepartmentModel.school_id == current_user.school_id,
        DepartmentModel.is_active == True
    ).all()
    
    result = []
    for dept in departments:
        # Lấy danh sách ID giáo viên thuộc khối này
        teacher_ids = [u.user_id for u in db.query(UserModel).filter(
            UserModel.department_id == dept.department_id,
            UserModel.school_id == current_user.school_id
        ).all()]
        
        if not teacher_ids:
            result.append({"department_name": dept.department_name, "score": 100.0})
            continue
            
        # Tính tổng điểm tích lũy của toàn bộ giáo viên trong khối
        total_delta = db.query(func.sum(KpiEventModel.score_delta)).filter(
            KpiEventModel.user_id.in_(teacher_ids)
        ).scalar() or 0
        
        # Công thức: (Số lượng GV * 100 điểm nền + Tổng biến động điểm) / Số lượng GV
        avg_score = (len(teacher_ids) * 100 + total_delta) / len(teacher_ids)
        
        result.append({
            "department_name": dept.department_name,
            "score": round(avg_score, 1)
        })
        
    return result