from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.evidence_repository import EvidenceRepository
from app.repositories.task_repository import TaskRepository
from app.models.evidence import Evidence
from datetime import datetime

class EvidenceService:
    def __init__(self, db: AsyncSession):
        self.evidence_repo = EvidenceRepository(db)
        self.task_repo = TaskRepository(db)

    async def submit_evidence(self, user_id: int, data: EvidenceCreate) -> Evidence:
        # Kiểm tra xem nhiệm vụ có tồn tại hay không
        task = await self.task_repo.get_by_id(data.task_id)
        if not task:
            raise ValueError("Nhiệm vụ không tồn tại!")
            
        # Kiểm tra quyền: Chỉ giáo viên được giao nhiệm vụ đó mới có quyền nộp minh chứng
        if task.assigned_to != user_id:
            raise PermissionError("Bạn không có quyền nộp minh chứng cho nhiệm vụ này!")

        # Không cho phép nộp minh chứng nếu việc đã nghiệm thu/bị hủy
        if task.status in ["COMPLETED", "FAILED", "CANCELLED"]:
            raise ValueError("Không thể nộp minh chứng cho nhiệm vụ đã đóng hoặc đã nghiệm thu!")

        # Khởi tạo thực thể minh chứng
        evidence = Evidence(
            task_id=data.task_id,
            uploaded_by=user_id,
            file_url=data.file_url,
            file_name=data.file_name,
            file_type=data.file_type,
            note=data.note,
            uploaded_at=datetime.utcnow()
        )
        
        # Nếu nhiệm vụ đang ở trạng thái PENDING, tự động chuyển sang RUNNING khi có minh chứng
        if task.status == "PENDING":
            task.status = "RUNNING"
            task.updated_at = datetime.utcnow()
            await self.task_repo.update(task)

        return await self.evidence_repo.create_evidence(evidence)

    async def get_task_evidences(self, task_id: int):
        return await self.evidence_repo.get_evidences_by_task(task_id)