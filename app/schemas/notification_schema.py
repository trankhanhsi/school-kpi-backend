from pydantic import BaseModel
from datetime import datetime

class NotificationResponse(BaseModel):
    notification_id: int
    user_id: int
    title: str
    content: str
    notification_type: str | None = None  # e.g., 'TASK_ASSIGNED', 'SCORE_AWARDED'
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True