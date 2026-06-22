from sqlalchemy import *
from app.models.base import Base

class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    notification_type = Column(String)
    is_read = Column(Boolean)
    created_at = Column(DateTime)
