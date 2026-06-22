from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.notification_repository import NotificationRepository
from app.models.notification import Notification
from datetime import datetime

class NotificationService:
    def __init__(self, db: AsyncSession):
        self.repo = NotificationRepository(db)

    async def send_notification(self, user_id: int, title: str, content: str, noti_type: str):
        """Hàm nội bộ dùng để tạo nhanh thông báo trong hệ thống"""
        now_naive = datetime.utcnow()
        
        noti = Notification(
            # Sinh ID ngẫu nhiên hoặc dựa trên timestamp (miliseconds) dạng số nguyên BigIngeger
            notification_id=int(now_naive.timestamp() * 1000),
            user_id=user_id,
            title=title,
            content=content,
            notification_type=noti_type,
            is_read=False,
            created_at=now_naive
        )
        return await self.repo.create_notification(noti)

    async def get_user_notifications(self, user_id: int):
        return await self.repo.get_by_user(user_id)

    async def read_notification(self, notification_id: int, user_id: int):
        # Đã sửa lại ký hiệu comment thành chuẩn Python (#)
        return await self.repo.mark_as_read(notification_id, user_id)