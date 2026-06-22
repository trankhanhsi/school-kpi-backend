from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task_template import TaskTemplate

class TemplateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_template(self, template: TaskTemplate) -> TaskTemplate:
        self.db.add(template)
        await self.db.flush()
        return template

    async def get_template_by_code(self, code: str) -> TaskTemplate | None:
        result = await self.db.execute(select(TaskTemplate).where(TaskTemplate.template_code == code))
        return result.scalar_one_or_none()

    async def get_active_templates(self):
        result = await self.db.execute(select(TaskTemplate).where(TaskTemplate.is_active == True))
        return result.scalars().all()