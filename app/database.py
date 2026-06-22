from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends
from typing import AsyncGenerator

# Chuỗi kết nối sử dụng asyncpg cho PostgreSQL bất đồng bộ
DATABASE_URL = "postgresql+asyncpg://postgres:93932406@localhost:5432/school_kpi_v2"

# Khởi tạo Engine Async
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False  # Đổi thành True nếu bạn muốn xem log câu lệnh SQL dưới Terminal
)

# Khởi tạo Session Factory tạo phiên làm việc Async
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Hàm Dependency cung cấp Session cho các API (Thay thế cho get_db cũ)
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()