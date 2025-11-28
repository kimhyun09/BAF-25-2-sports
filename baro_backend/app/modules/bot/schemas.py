from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    user_lat: Optional[float] = None
    user_lon: Optional[float] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    goal_weight_kg: Optional[float] = None
    weekly_goal_kg: Optional[float] = None

class ChatResponse(BaseModel):
    answer: str