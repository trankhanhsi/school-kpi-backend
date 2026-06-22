from sqlalchemy import *
from app.models.base import Base

class TaskComment(Base):
    __tablename__ = "task_comments"

    comment_id = Column(BigInteger, primary_key=True, nullable=False)
    task_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime)
