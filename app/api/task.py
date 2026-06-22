from fastapi import APIRouter, Depends, HTTPException
from app.database import get_async_db, AsyncSession
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskCompleteRequest
from app.services.task_service import TaskService
from app.dependencies.auth_dependency import get_current_user_id

router = APIRouter()

@router.post("/")
async def create_task(
    data: TaskCreate,
    current_user: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db)
):
    service = TaskService(db)
    # 1. Gọi service khởi tạo task và tự động sinh bản ghi thông báo trong Session
    new_task = await service.create_task(
        title=data.title,
        description=data.description,
        assigned_to=data.assigned_to,
        assigned_by=current_user,
        deadline=data.deadline,
        priority=data.priority,
        score_value=data.score_value
    )
    
    # 2. ÉP BUỘC COMMIT: Đồng bộ vĩnh viễn cả Task và Notification xuống Database
    await db.commit()
    
    # 3. Làm tươi lại object (nếu cần lấy ID tự sinh từ DB sau commit)
    await db.refresh(new_task)
    
    return new_task

@router.get("/")
async def get_tasks(db: AsyncSession = Depends(get_async_db)):
    service = TaskService(db)
    return await service.get_tasks()

@router.get("/{task_id}")
async def get_task(task_id: int, db: AsyncSession = Depends(get_async_db)):
    service = TaskService(db)
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/{task_id}/start")
async def start_task(task_id: int, db: AsyncSession = Depends(get_async_db)):
    service = TaskService(db)
    task = await service.start_task(task_id)
    if not task:
        raise HTTPException(status_code=400, detail="Cannot start task")
    
    # Commit trạng thái RUNNING xuống DB
    await db.commit()
    return task

@router.post("/{task_id}/complete")
async def complete_task(task_id: int, data: TaskCompleteRequest, db: AsyncSession = Depends(get_async_db)):
    service = TaskService(db)
    task = await service.complete_task(task_id, data.final_score)
    if not task:
        raise HTTPException(status_code=400, detail="Cannot complete task")
    
    # Commit trạng thái COMPLETED và điểm KPI mới xuống DB
    await db.commit()
    return task