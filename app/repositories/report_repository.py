from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.kpi_summary_monthly import KPISummaryMonthly
from app.models.user import User

class ReportRepository:

    @staticmethod
    async def get_school_leaderboard(db: AsyncSession, year: int, month: int):
        """
        Truy vấn danh sách xếp hạng thi đua toàn trường trong tháng/năm chỉ định
        Sắp xếp theo thứ tự điểm số giảm dần
        """
        stmt = (
            select(
                User.user_id,
                User.full_name,
                User.department_id,
                KPISummaryMonthly.total_score
            )
            .join(KPISummaryMonthly, User.user_id == KPISummaryMonthly.user_id)
            .where(
                KPISummaryMonthly.year == year,
                KPISummaryMonthly.month == month,
                User.is_active == True
            )
            .order_by(desc(KPISummaryMonthly.total_score))
        )
        
        result = await db.execute(stmt)
        return result.all()