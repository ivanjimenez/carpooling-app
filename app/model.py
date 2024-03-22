from pydantic import BaseModel, Field, validator
from typing import List, Optional, ClassVar, Set


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
            self.seats = self.seats - passengers

    def deallocate(self, passengers: int):
        self.seats = self.seats + passengers

    def can_allocate(self, passengers: int) -> bool:
        return self.seats >= passengers
    
    
class Group(BaseModel):
    id: int = Field(...,ge=1)
    seats: int = Field(..., ge=1, le=6)
    car_assigned: Optional[Car] = None

class Journey(BaseModel):
    groups: List[Group] = []

    def add_group(self, group: Group):
        self.groups.append(group)

    def remove_group_by_id(self, group_id: int):
        self.groups = [grp for grp in self.groups if grp.id != group_id]
  
    def get_all_group_ids(self):
        """
        Retorna una lista de todos los IDs de los grupos en el viaje.
        """
        return [group.id for group in self.groups]
    
    def get_group_by_id(self, group_id: int):
        """
        Retorna el elemento de grupo por ID de grupo.
        Si no se encuentra ningún grupo con el ID especificado, retorna None.
        """
        for group in self.groups:
            if group.id == group_id:
                return group
        return None
    