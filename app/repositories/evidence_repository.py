from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.evidence import Evidence

class EvidenceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_evidence(self, evidence: Evidence) -> Evidence:
        self.db.add(evidence)
        await self.db.flush()
        return evidence

    async def get_evidences_by_task(self, task_id: int):
        result = await self.db.execute(
            select(Evidence).where(Evidence.task_id == task_id).order_by(Evidence.uploaded_at.desc())
        )
        return result.scalars().all()