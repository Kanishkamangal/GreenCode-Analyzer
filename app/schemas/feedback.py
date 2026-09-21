from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class FeedbackCreate(BaseModel):
    user_id: int
    rating: Optional[int] = None
    category: str
    feedback_text: Optional[str] = None


class FeedbackResponse(BaseModel):
    feedback_id: int
    user_id: int
    rating: Optional[int]
    category: str
    feedback_text: Optional[str]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
