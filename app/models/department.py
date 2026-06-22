from sqlalchemy import *
from app.models.base import Base

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(BigInteger, primary_key=True, nullable=False)
    school_id = Column(BigInteger, nullable=False)
    department_name = Column(String, nullable=False)
    department_code = Column(String)
    manager_user_id = Column(BigInteger)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
