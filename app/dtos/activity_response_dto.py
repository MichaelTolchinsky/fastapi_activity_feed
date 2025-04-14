from pydantic import BaseModel
from datetime import datetime


class ActivityResponseDTO(BaseModel):
    id: int
    user_id: int
    action: str
    target_id: int
    timestamp: datetime

    model_config = {"from_attributes": True}
