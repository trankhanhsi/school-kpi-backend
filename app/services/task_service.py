from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.services.kpi_service import KPIService
from app.services.notification_service import NotificationService
from app.models.task import Task
from datetime import datetime, timezone

class TaskService:
    def __init__(self, db: AsyncSession):
        self.task_repo = TaskRepository(db)
        self.kpi_service = KPIService(db)
        self.notification_service = NotificationService(db)

    async def create_task(self, title: str, description: str, assigned_to: int, assigned_by: int, deadline: datetime, priority: str, score_value: int) -> Task:
        # Sử dụng datetime.now(timezone.utc).replace(tzinfo=None) để lấy naive UTC, tránh DeprecationWarning
        now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        
        task = Task(
            title=title,
            description=description,
            assigned_to=assigned_to,
            assigned_by=assigned_by,
            deadline=deadline,
            priority=priority,
            score_value=score_value,
            status="PENDING",
            created_at=now_naive,
            updated_at=now_naive
        )
        
        # 1. Lưu nhiệm vụ vào cơ sở dữ liệu (đưa vào Session quản lý)
        created_task = await self.task_repo.create(task)
        
        # ÉP BUỘC FLUSH: Đồng bộ trạng thái xuống DB ngay để lấy khóa ngoại, tránh lỗi cô lập transaction khi test
        await self.task_repo.db.flush()
        
        # 2. Tự động gửi thông báo đến giáo viên được giao việc (không làm block luồng chính)
        try:
            await self.notification_service.send_notification(
                user_id=assigned_to,
                title="🎯 Bạn có nhiệm vụ mới được giao",
                content=f"Nhiệm vụ: '{title}' đã được giao cho bạn. Vui lòng kiểm tra và thực hiện đúng hạn.",
                noti_type="TASK_ASSIGNED"
            )
            # Tiếp tục flush thông báo để đảm bảo dữ liệu sẵn sàng trong phiên làm việc
            await self.task_repo.db.flush()
        except Exception as e:
            # Ghi log lỗi thông báo nếu có nhưng không làm sập luồng tạo task chính
            print(f"⚠️ Cảnh báo: Không thể gửi thông báo tự động: {e}")

        return created_task

    async def get_tasks(self):
        return await self.task_repo.get_all()

    async def get_task(self, task_id: int) -> Task | None:
        return await self.task_repo.get_by_id(task_id)

    async def start_task(self, task_id: int) -> Task | None:
        task = await self.task_repo.get_by_id(task_id)
        if not task or task.status != "PENDING":
            return None
            
        now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        task.status = "RUNNING"
        task.updated_at = now_naive
        return await self.task_repo.update(task)

    async def complete_task(self, task_id: int, final_score: int) -> Task | None:
        """
        Nghiệm thu hoàn thành nhiệm vụ và kích hoạt KPI Engine tự động cộng điểm thi đua
        """
        task = await self.task_repo.get_by_id(task_id)
        if not task or task.status not in ["PENDING", "RUNNING"]:
            return None

        now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
        
        # Cập nhật trạng thái nhiệm vụ hoàn thành
        task.status = "COMPLETED"
        task.final_score = final_score
        task.updated_at = now_naive
        await self.task_repo.update(task)

        # Kích hoạt KPI Engine: Sinh sự kiện ghi nhận điểm thi đua cho giáo viên
        await self.kpi_service.add_score(
            user_id=task.assigned_to,
            rule_id=1,  # Gán mặc định ID Rule nghiệm thu nhiệm vụ
            task_id=task.task_id,
            score_delta=final_score,
            note=f"Cộng điểm hoàn thành nhiệm vụ: {task.title}"
        )

        return task