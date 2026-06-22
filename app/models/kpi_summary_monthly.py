from sqlalchemy import Column, BigInteger, Integer, Numeric, DateTime, func
from app.models.base import Base

class KPISummaryMonthly(Base):
    __tablename__ = "kpi_summary_monthly"

    summary_id = Column(
        BigInteger, 
        primary_key=True
    )
    
    # Thêm index=True để tăng tốc độ tìm kiếm báo cáo theo user
    user_id = Column(
        BigInteger, 
        nullable=False, 
        index=True
    )
    
    year = Column(
        Integer, 
        nullable=False
    )
    
    month = Column(
        Integer, 
        nullable=False
    )
    
    # Định nghĩa precision/scale để đảm bảo độ chính xác cho số thập phân
    total_score = Column(
        Numeric(10, 2), 
        default=0
    )
    
    rank_school = Column(
        Integer
    )
    
    rank_department = Column(
        Integer
    )
    
    # Tự động lấy thời điểm hệ thống tạo record
    calculated_at = Column(
        DateTime, 
        default=func.now()
    )