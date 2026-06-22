from sqlalchemy import *
from app.models.base import Base

class TaskTemplate(Base):
    __tablename__ = "task_templates"

    template_id = Column(BigInteger, primary_key=True, nullable=False)
    school_id = Column(BigInteger, nullable=False)
    template_code = Column(String, nullable=False)
    template_name = Column(String, nullable=False)
    description = Column(Text)
    frequency = Column(String, nullable=False)
    default_score = Column(Integer)
    auto_generate = Column(Boolean)
    deadline_rule = Column(String)
    target_role = Column(String)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
