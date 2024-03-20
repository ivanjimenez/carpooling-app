import logging
from typing import List, Dict

import app.model as model
from app.model import Group


class ServiceError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class GroupDoesNotExistError(ServiceError):
    """Raised when a group does not exist

    """

    def __init__(self, group_id: int):
        super().__init__(f"The group {group_id} does not exist")


class Service:
    def __init__(self):
        self.cars: Dict[int, model.Car] = {}
        self.groups: List[model.Group] = []

    def add_cars(self, cars: List[model.Car]) -> None:
        logging.debug(f"Adding {cars=}")
        self.cars = {}
        self.groups = []
        for car in cars:
            if self.cars.get(car.id, False):
                raise ValueError(f'{car.id} is a repeated car ID')
            if car.max_seats < 4 or car.max_seats > 6:
                self.cars = {}
                self.groups = []
                raise ValueError(f'{car.max_seats} is not a valid seats number')
            self.cars[car.id] = car

    def get_cars(self) -> List[model.Car]:
        return list(self.cars.values())

    def add_car(self, car):
        self.cars[car.id] = car

    def get_car(self, car_id) -> model.Car:
        return self.cars.get(car_id)

    def del_car(self, car_id):
        try:
            del self.cars[car_id]
        except KeyError:
            pass

    def add_groups(self, groups: List[Group]):
        logging.debug(f"Adding {groups=}")
        self.groups = groups

    def get_groups(self) -> List[Group]:
        return self.groups

    def add_group(self, group: Group):
        self.groups.append(group)

    def get_group(self, group_id: int) -> Group:
        logging.debug(f"Find group with {group_id=}")
        for group in self.groups:
            if group.Id == group_id:
                return group
        logging.debug(f"Groups {self.groups}")
        raise GroupDoesNotExistError(group_id)

    def del_group(self, group_id) -> bool:
        """Deleting a group from the de service.

        :param group_id: The id of the group to be deleted.
        :return: True if the group was deleted.
        :raise: GroupDoesNotExistError if the group does not exist.
        """
        for ix, group in enumerate(self.groups):
            if group.Id == group_id:
                del self.groups[ix]
                return True
        raise GroupDoesNotExistError(group_id)

    def journey(self, group_id: int, passengers: int) -> None:
        logging.debug(f"Journey for group {group_id} with {passengers} passenger")
        try:
            group = self.get_group(group_id)
        except GroupDoesNotExistError:
            group = Group(group_id, passengers)
            self.add_group(group)

        if group.assigned_to:
            return None

        car = self.find_car(group.passengers)
        if car:
            car.allocate(group.passengers)
            group.assigned_to = car

        logging.debug(f"Setup journey for {group=}")

    def drop_off(self, group_id: int) -> bool:
        """Drop a group from the service.

        :param group_id: The group id to be deleted
        :return: True if the group was successfully dropped
        :raise: GroupDoesNotExistError if the group does not exist
        """
        group = self.get_group(group_id)
        if group.assigned_to:
            group.assigned_to.deallocate(group.passengers)

        logging.debug(f"Dropping group {group=}")
        return self.del_group(group_id)

    def find_car(self, seats: int):
        sorted_cars = dict(sorted(self.cars.items(), key=lambda x: x[1].seats))
        for car in sorted_cars.values():
            if car.can_allocate(seats):
                return car
        return None

    def reassign(self):
        groups = self.get_groups()

        for group in groups:
            if not group.assigned_to:
                car = self.find_car(group.passengers)
                if car:
                    car.allocate(group.passengers)
                    group.assigned_to = car
