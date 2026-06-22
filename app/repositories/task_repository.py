from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task: Task) -> Task:
        self.db.add(task)
        await self.db.flush()  # Sinh ID tự động mà không cần commit ngay
        return task

    async def get_by_id(self, task_id: int) -> Task | None:
        result = await self.db.execute(select(Task).where(Task.task_id == task_id))
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(select(Task))
        return result.scalars().all()

    async def update(self, task: Task) -> Task:
        await self.db.flush()
        return task

    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.flush()