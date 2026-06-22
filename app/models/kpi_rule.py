from sqlalchemy import *
from app.models.base import Base

class KpiRule(Base):
    __tablename__ = "kpi_rules"

    rule_id = Column(BigInteger, primary_key=True, nullable=False)
    school_id = Column(BigInteger, nullable=False)
    rule_code = Column(String, nullable=False)
    rule_name = Column(String, nullable=False)
    description = Column(Text)
    score_value = Column(Integer, nullable=False)
    target_role = Column(String)
    auto_apply = Column(Boolean)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
