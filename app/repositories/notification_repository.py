from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification

class NotificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_notification(self, noti: Notification) -> Notification:
        self.db.add(noti)
        await self.db.flush()
        return noti

    async def get_by_user(self, user_id: int):
        """Lấy danh sách thông báo của user, mới nhất xếp lên đầu"""
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(desc(Notification.created_at))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def mark_as_read(self, notification_id: int, user_id: int) -> bool:
        stmt = select(Notification).where(
            Notification.notification_id == notification_id, 
            Notification.user_id == user_id
        )
        result = await self.db.execute(stmt)
        noti = result.scalar_one_or_none()
        if noti:
            noti.is_read = True
            await self.db.flush()
            return True
        return False