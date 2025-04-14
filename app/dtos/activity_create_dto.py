from pydantic import BaseModel
from datetime import datetime


class ActivityCreateDTO(BaseModel):
    user_id: int
    action: str
    target_id: int
    timestamp: datetime
