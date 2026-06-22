from sqlalchemy import *
from app.models.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(BigInteger, primary_key=True, nullable=False)
    actor_user_id = Column(BigInteger)
    action_type = Column(String)
    object_type = Column(String)
    object_id = Column(BigInteger)
    description = Column(Text)
    ip_address = Column(String)
    created_at = Column(DateTime)
