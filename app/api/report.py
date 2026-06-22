from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.services.report_service import ReportService
from datetime import datetime

router = APIRouter()

@router.get("/leaderboard/school")
async def get_school_leaderboard(
    year: int | None = None,
    month: int | None = None,
    db: AsyncSession = Depends(get_async_db)
):
    # Nếu không truyền year/month, hệ thống tự động lấy tháng năm hiện tại
    now = datetime.utcnow()
    target_year = year or now.year
    target_month = month or now.month
    
    service = ReportService(db)
    report_data = await service.generate_monthly_school_report(year=target_year, month=target_month)
    
    return {
        "year": target_year,
        "month": target_month,
        "total_records": len(report_data),
        "leaderboard": report_data
    }
