from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.template_repository import TemplateRepository
from app.models.task_template import TaskTemplate

class TemplateService:
    def __init__(self, db: AsyncSession):
        self.repo = TemplateRepository(db)

    async def create_new_template(self, data: TemplateCreate) -> TaskTemplate:
        existing = await self.repo.get_template_by_code(data.template_code)
        if existing:
            raise ValueError("Mã mẫu nhiệm vụ này đã tồn tại trong hệ thống!")
            
        template = TaskTemplate(
            school_id=data.school_id,
            template_code=data.template_code,
            template_name=data.template_name,
            description=data.description,
            frequency=data.frequency,
            default_score=data.default_score,
            target_role=data.target_role,
            is_active=True
        )
        return await self.repo.create_template(template)

    async def list_active_templates(self):
        return await self.repo.get_active_templates()