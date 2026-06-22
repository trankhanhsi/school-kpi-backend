from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.kpi_repository import KPIRepository
from app.models.kpi_event import KPIEvent
from app.models.kpi_summary_monthly import KPISummaryMonthly
from datetime import datetime

class KPIService:
    def __init__(self, db: AsyncSession):
        self.kpi_repo = KPIRepository(db)

    async def add_score(self, user_id: int, rule_id: int, task_id: int, score_delta: int, note: str) -> KPIEvent:
        """
        Sinh một sự kiện điểm số KPI Event mới khi có biến động điểm (Thành tích, vi phạm, nhiệm vụ...)
        """
        # 1. Khởi tạo event mới
        event = KPIEvent(
            user_id=user_id,
            rule_id=rule_id,
            task_id=task_id,
            score_delta=score_delta,
            note=note,
            created_at=datetime.utcnow()
        )
        await self.kpi_repo.create_event(event)

        # 2. Tự động cập nhật hoặc lũy kế vào bảng tổng hợp tháng (KPI Summary Monthly)
        now = datetime.utcnow()
        summary = await self.kpi_repo.get_month_summary(user_id, now.year, now.month)

        if not summary:
            # Nếu tháng này chưa có bản ghi tổng hợp, khởi tạo với điểm nền ban đầu là 100
            summary = KPISummaryMonthly(
                user_id=user_id,
                year=now.year,
                month=now.month,
                total_score=100.00 + score_delta,
                calculated_at=datetime.utcnow()
            )
            await self.kpi_repo.create_summary(summary)
        else:
            # Nếu đã tồn tại bản ghi tháng, tiến hành cộng dồn / trừ bớt điểm vào tổng điểm
            summary.total_score = float(summary.total_score) + score_delta
            summary.calculated_at = datetime.utcnow()
            await self.kpi_repo.update_summary(summary)

        return event