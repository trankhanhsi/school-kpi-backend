from sqlalchemy import *
from app.models.base import Base

class Evidence(Base):
    __tablename__ = "evidences"

    evidence_id = Column(BigInteger, primary_key=True, nullable=False)
    task_id = Column(BigInteger, nullable=False)
    uploaded_by = Column(BigInteger, nullable=False)
    file_url = Column(Text, nullable=False)
    file_name = Column(String)
    file_type = Column(String)
    note = Column(Text)
    uploaded_at = Column(DateTime)
