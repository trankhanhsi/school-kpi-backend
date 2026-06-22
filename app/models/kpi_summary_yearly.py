from sqlalchemy import *
from app.models.base import Base

class KpiSummaryYearly(Base):
    __tablename__ = "kpi_summary_yearly"

    summary_id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    year = Column(Integer, nullable=False)
    total_score = Column(String)
    final_grade = Column(String)
    rank_school = Column(Integer)
    calculated_at = Column(DateTime)
