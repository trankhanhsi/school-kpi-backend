from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.schemas.notification_schema import NotificationResponse
from app.services.notification_service import NotificationService
from app.dependencies.auth_dependency import get_current_user_id

router = APIRouter()

@router.get("/", response_model=list[NotificationResponse])
async def get_my_notifications(
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db)
):
    service = NotificationService(db)
    return await service.get_user_notifications(user_id=current_user_id)

@router.post("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_db)
):
    service = NotificationService(db)
    success = await service.read_notification(notification_id, user_id=current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông báo hoặc bạn không có quyền.")
    return {"status": "success", "message": "Đã đánh dấu đọc thông báo."}