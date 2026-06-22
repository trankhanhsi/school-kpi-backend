from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.kpi_event import KPIEvent
from app.models.kpi_summary_monthly import KPISummaryMonthly

class KPIRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event(self, event: KPIEvent) -> KPIEvent:
        self.db.add(event)
        await self.db.flush()
        return event

    async def get_month_summary(self, user_id: int, year: int, month: int) -> KPISummaryMonthly | None:
        stmt = select(KPISummaryMonthly).where(
            KPISummaryMonthly.user_id == user_id,
            KPISummaryMonthly.year == year,
            KPISummaryMonthly.month == month
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_summary(self, summary: KPISummaryMonthly) -> KPISummaryMonthly:
        self.db.add(summary)
        await self.db.flush()
        return summary

    async def update_summary(self, summary: KPISummaryMonthly) -> KPISummaryMonthly:
        await self.db.flush()
        return summary