from pydantic import BaseModel, Field, validator
from typing import List

class Car(BaseModel):
    
    id: int = Field(...,ge=1)
    seats: int = Field(...,ge=4, le=6)

class Group(BaseModel):
    id: int = Field(...,ge=1)
    people: int = Field(..., ge=1, le=6)

class Journey(BaseModel):
    id: int
    groups: List[Group]