from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    
    # AuthUser 필드와 매칭 (alias는 프론트엔드 변수명)
    nickname: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = Field(None, alias="birthDate") # "YYYY-MM-DD"
    
    height: Optional[float] = None
    weight: Optional[float] = None
    muscle_mass: Optional[float] = Field(None, alias="muscleMass")
    
    skill_level: Optional[str] = Field(None, alias="skillLevel")
    favorite_sports: Optional[List[str]] = Field(default=[], alias="favoriteSports")
    
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        populate_by_name = True 

class ChatResponse(BaseModel):
    answer: str