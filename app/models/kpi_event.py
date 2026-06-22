from sqlalchemy import *
from app.models.base import Base
from datetime import datetime  # Nên import thêm thư viện này

class KPIEvent(Base):
    __tablename__ = "kpi_events"

    event_id = Column(
        BigInteger,
        primary_key=True
    )

    user_id = Column(
        BigInteger,
        nullable=False
    )

    rule_id = Column(
        BigInteger
    )

    task_id = Column(
        BigInteger
    )

    score_delta = Column(
        Integer,
        nullable=False
    )

    note = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow  # Gợi ý: Thêm giá trị mặc định để tự động lấy thời gian
    )