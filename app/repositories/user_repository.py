from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

class UserRepository:

    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: int):
        stmt = select(User).where(User.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str):
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_active_users(db: AsyncSession):
        stmt = select(User).where(User.is_active == True)
        result = await db.execute(stmt)
        return result.scalars().all()