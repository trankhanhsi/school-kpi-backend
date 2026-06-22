from sqlalchemy import BigInteger, Date, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    profile_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True)
    date_of_birth = mapped_column(Date, nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    position_title: Mapped[str] = mapped_column(String(255), nullable=True)
    professional_rank: Mapped[str] = mapped_column(String(100), nullable=True)
    degree: Mapped[str] = mapped_column(String(255), nullable=True)
    homeroom_class: Mapped[str] = mapped_column(String(50), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="profile")