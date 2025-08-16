from pydantic import BaseModel
from typing import List, Optional

class Recommendation(BaseModel):
    item_id: int
    score: float
    reason: str

class HomefeedResponse(BaseModel):
    user_id: int
    recommendations: List[Recommendation]

class Feedback(BaseModel):
    user_id: int
    item_id: int
    feedback_type: str  
