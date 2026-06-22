from sqlalchemy import *
from app.models.base import Base

class SchedulerJob(Base):
    __tablename__ = "scheduler_jobs"

    job_id = Column(BigInteger, primary_key=True, nullable=False)
    template_id = Column(BigInteger, nullable=False)
    frequency = Column(String)
    next_run = Column(DateTime)
    last_run = Column(DateTime)
    enabled = Column(Boolean)
    created_at = Column(DateTime)
