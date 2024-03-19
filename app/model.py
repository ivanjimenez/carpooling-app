from pydantic import BaseModel, Field, validator
from typing import List, Optional, ClassVar


class Car(BaseModel):
    id: int = Field(..., ge=1)
    seats: int = Field(..., ge=4, le=6)

    # Atributo de clase para mantener un registro de IDs ya asignadas
    assigned_ids: ClassVar[set] = set()

    def __init__(self, **data):
        super().__init__(**data)
        # Verifica si la ID ya está asignada a otra instancia
        if self.id in self.__class__.assigned_ids:
            raise ValueError(f"ID {self.id} ya está asignada a otra instancia")
        # Agrega la ID a las IDs asignadas
        self.__class__.assigned_ids.add(self.id)

    def allocate(self, passengers: int):
        if self.can_allocate(passengers):
            self.free_seats = self.free_seats - passengers

    def deallocate(self, passengers: int):
        self.free_seats = self.free_seats + passengers

    def can_allocate(self, passengers: int) -> bool:
        return self.free_seats >= passengers
    
    
class Group(BaseModel):
    id: int = Field(...,ge=1)
    people: int = Field(..., ge=1, le=6)
    car_assigned: Optional[Car]

class Journey(BaseModel):
    id: int
    _groups_ids: set = set()  # Conjunto para almacenar las IDs únicas de los grupos

    groups: List[Group]

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, value):
        for group in value:
            if group.id in self._groups_ids:
                raise ValueError(f"La ID {group.id} ya está en uso en la lista de grupos")
            self._groups_ids.add(group.id)
        self._groups = value

    def is_group_id_present(self, group_id: int) -> bool:
        """Verifica si una ID de grupo está presente en la lista de grupos."""
        return group_id in self._groups_ids