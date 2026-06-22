from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task_service import TaskService
from app.repositories.template_repository import TemplateRepository
from app.repositories.user_repository import UserRepository
from datetime import datetime, timedelta

class SchedulerService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.template_repo = TemplateRepository(db)
        self.user_repo = UserRepository()
        self.task_service = TaskService(db)

    async def trigger_cron_generation(self, school_id: int, assigned_by_admin_id: int):
        """
        Hàm cốt lõi mô phỏng một lượt quét của CronJob hệ thống:
        Tự động lấy các mẫu nhiệm vụ định kỳ và tạo tác vụ thực tế cho toàn bộ giáo viên đang hoạt động.
        """
        # 1. Lấy danh sách mẫu nhiệm vụ đang kích hoạt
        templates = await self.template_repo.get_active_templates()
        
        # 2. Lấy danh sách giáo viên đang hoạt động tại trường để giao việc
        active_teachers = await self.user_repo.get_active_users(self.db)
        
        generated_count = 0
        now = datetime.utcnow()

        for template in templates:
            if template.school_id != school_id:
                continue
                
            # Tính toán thời hạn hoàn thành (deadline) tự động dựa trên tần suất mẫu
            if template.frequency == "WEEKLY":
                calculated_deadline = now + timedelta(days=7)
            elif template.frequency == "MONTHLY":
                calculated_deadline = now + timedelta(days=30)
            else:
                calculated_deadline = now + timedelta(days=2) # Mặc định hoặc các hạn định khác

            # 3. Tiến hành phân rã và sinh việc tự động cho từng giáo viên
            for teacher in active_teachers:
                # Tránh trường hợp admin tự giao việc cho chính mình nếu admin cũng nằm trong danh sách hoạt động
                if teacher.user_id == assigned_by_admin_id:
                    continue

                await self.task_service.create_task(
                    title=f"[{template.frequency}] {template.template_name}",
                    description=f"Nhiệm vụ tự động sinh từ hệ thống. {template.description or ''}",
                    assigned_to=teacher.user_id,
                    assigned_by=assigned_by_admin_id,
                    deadline=calculated_deadline,
                    priority="NORMAL",
                    score_value=template.default_score
                )
                generated_count += 1

        return generated_count