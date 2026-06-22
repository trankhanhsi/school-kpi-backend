from sqlalchemy import BigInteger, String, Text, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    template_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    assigned_to: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    assigned_by: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), nullable=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    deadline: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="PENDING")
    priority: Mapped[str] = mapped_column(String(20), default="NORMAL")
    score_value: Mapped[int] = mapped_column(Integer, default=0)
    final_score: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())