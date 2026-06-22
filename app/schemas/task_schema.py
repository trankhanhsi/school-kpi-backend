from pydantic import BaseModel
from datetime import datetime

class TaskCompleteRequest(BaseModel):
    final_score: int
    
class TaskCreate(BaseModel):

    title: str

    description: str | None = None

    assigned_to: int

    deadline: datetime | None = None

    priority: str = "normal"

    score_value: int = 0


class TaskUpdate(BaseModel):

    title: str | None = None

    description: str | None = None

    deadline: datetime | None = None

    priority: str | None = None

    status: str | None = None

    final_score: int | None = None


class TaskResponse(BaseModel):

    task_id: int

    title: str

    description: str | None = None

    assigned_to: int

    assigned_by: int | None = None

    status: str | None = None

    priority: str | None = None

    score_value: int | None = None

    final_score: int | None = None

    created_at: datetime | None = None

    updated_at: datetime | None = None

    class Config:
        from_attributes = True