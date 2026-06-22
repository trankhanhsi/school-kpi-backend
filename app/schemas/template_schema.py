from pydantic import BaseModel
from datetime import datetime

class TemplateCreate(BaseModel):
    school_id: int
    template_code: str
    template_name: str
    description: str | None = None
    frequency: str  # e.g., 'WEEKLY', 'MONTHLY'
    default_score: int = 0
    target_role: str | None = None

class TemplateResponse(BaseModel):
    template_id: int
    school_id: int
    template_code: str
    template_name: str
    description: str | None = None
    frequency: str
    default_score: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True