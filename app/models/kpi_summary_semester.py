from sqlalchemy import *
from app.models.base import Base

class KpiSummarySemester(Base):
    __tablename__ = "kpi_summary_semester"

    summary_id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    year = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    total_score = Column(String)
    rank_school = Column(Integer)
    calculated_at = Column(DateTime)
