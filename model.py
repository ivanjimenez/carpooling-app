from pydantic import BaseModel, Field, validator
from typing import List
from typing import Optional



class Car(BaseModel):
    
    id: int = Field(...,ge=1)
    max_seats: int = Field(...,ge=4, le=6)
    free_seats: int
    
    def allocate(self, passengers : int):
        if self.can_allocate(passengers):
            self.free_seats = self.free_seats - passengers
    
    def deallocate(self, passengers: int):
        self.free_seats = self.free_seats + passengers
    
    def can_allocate(self, passengers) -> bool:
        return self.free_seats >= passengers

class Group(BaseModel):
    id: int = Field(...,ge=1)
    people: int = Field(..., ge=1, le=6)
    assigned_to: Optional[Car]

class Journey(BaseModel):
    id: int
    groups: List[Group]
