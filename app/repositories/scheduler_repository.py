from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.scheduler_job import SchedulerJob

class SchedulerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_pending_jobs(self):
        """Lấy các tác vụ lập lịch đang kích hoạt"""
        result = await self.db.execute(
            select(SchedulerJob).where(SchedulerJob.is_active == True)
        )
        return result.scalars().all()

    async def update_job_status(self, job: SchedulerJob) -> SchedulerJob:
        await self.db.flush()
        return job