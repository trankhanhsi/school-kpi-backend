from pydantic import BaseModel
from datetime import datetime

class EvidenceCreate(BaseModel):
    task_id: int
    file_url: str
    file_name: str | None = None
    file_type: str | None = None
    note: str | None = None

class EvidenceResponse(BaseModel):
    evidence_id: int
    task_id: int
    uploaded_by: int
    file_url: str
    file_name: str | None = None
    file_type: str | None = None
    note: str | None = None
    uploaded_at: datetime

    class Config:
        from_attributes = True