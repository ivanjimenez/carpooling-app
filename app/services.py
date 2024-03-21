from app.priority_queue import PriorityQueue
from app.model import Car, Group, Journey

from fastapi import HTTPException, Response
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

import logging
from typing import List

class Application:

     # Global variables to store car data and journey information
    LOW_PRIORITY = 1
    MID_PRIORITY = 5
    HIGH_PRIORITY = 7

    def __init__(self):

        self.journeys  = Journey()
        self.cars : List[Car] = []
        self.grouplist = PriorityQueue()

    def add_cars(self, car_list: List[Car], req : Request):

        # if req.headers != 'application/json':
        #     raise HTTPException(status_code=400, detail="Bad Request")

        # for car in car_list:
        #     if car.id < 1 or not (4 <= car.seats <= 6):
        #         raise HTTPException(status_code=400, detail="Bad Request")

        try:
            self.cars = car_list


        except Exception:
            raise HTTPException(status_code=400, detail="Bad Request")

        logging.debug(f"Cars Queue: {self.cars}")
        return Response(status_code=HTTP_200_OK)

    def add_journey(self, group : Group):

        """
        Vale aquí serían los siguientes pasos
        1. Una vez hecha la petición y almacenado el grupo tal vez había que meterlos con el modelo Group, 
        pero no lo vamos a encolar porque si no hay sitio tendremos que usar otra prioridad. 
        2. Después debe iterar sobre la lista de coches y de aquellos que están disponibles, buscar el coche
        que tenga sitios libres para el viaje. 
        3. En caso de no tener sitio se inserta con una prioridad  + 1, hay que tener en cuenta que igual este grupo
        no encuentra varias veces sitio y se tiene que ir. 
        4. De hecho si le ha pasado más veces asignamos una de +5, así nos aseguramos que no desista.
        5. Si ha encontrado sitio asignamos el coche al grupo y restamos los sitios libres del grupo, como no se puede
        usar otro viaje a la vez nos quedamos así.
        """

        """
        Este método intenta asignar un grupo a un coche disponible.
        Si no hay coches disponibles, encola el grupo en la cola prioritaria.
        """
        try:
            group_model = Group(**group)

            # Intentar asignar un coche disponible
            car_assigned = None
            for car in self.cars:
                if car.can_allocate(group_model.people):
                    car.allocate(group_model.people)
                    group_model.car_assigned = car
                    self.journeys.add_group(group_model)
                    logging.info("Group assigned to a car.")
                    self.print_queue()
                    return Response(status_code=HTTP_200_OK)

            # Si no se asigna a un coche, encolar en la cola prioritaria
            self.grouplist.enqueue_with_priority(self.LOW_PRIORITY, group_model)
            logging.info("Group enqueued in priority queue.")
            self.print_queue()


            # Intentar asignar coches a grupos en la cola prioritaria
            self.assign_cars_to_priority_groups()

        except Exception as e:
            logging.exception("An exception")
            raise HTTPException(status_code=400, detail="Bad Request")

        return Response(status_code=HTTP_200_OK)

    def print_queue(self):
        logging.info(f"Journeys: {self.journeys.groups}")
        logging.info(f"PriorityQueue: {self.grouplist._elements}")
        logging.info(f"Cars Avail: {self.cars}")

    def assign_cars_to_priority_groups(self):
        """
        Este método intenta asignar coches a grupos en la cola prioritaria.
        """
        unassigned_groups = []  # Lista para almacenar temporalmente grupos no asignados

        # Intentamos asignar coches a grupos en la cola prioritaria
        while not self.grouplist.is_empty():
            group = self.grouplist.dequeue()
            assigned = False

            # Intentamos asignar el grupo a un coche
            for car in self.cars:
                if car.can_allocate(group.people):
                    car.allocate(group.people)
                    group.car_assigned = car
                    self.journeys.add_group(group)
                    logging.info("Priority group assigned to a car.")
                    assigned = True
                    break

            # Si no se puede asignar, añadimos el grupo a la lista de no asignados
            if not assigned:
                unassigned_groups.append(group)

        # Devolvemos los grupos no asignados a la cola prioritaria
        for group in unassigned_groups:
            self.grouplist.enqueue_with_priority(self.HIGH_PRIORITY, group)

        # Si no hay coches disponibles, informamos
        if not assigned:
            logging.info("No available cars for priority groups.")

    def drop_off(self, group_id : int):
        """
        1. Búsqueda por ID en la lista de grupos y verificar si está viajando, pues si no está viajando
        no tiene sentido borrarlo
        2. Si está viajando querrá decir que finalizamos viaje. Es decir, que liberamos los sitios del coche
        y borramos el grupo de personas.
        """
        try:

            # Test if group id is in priorityqueue or is in journey
            pq_group_id :bool = group_id in self.grouplist.get_group_ids()
            model_group_id : bool = group_id in self.journeys.get_all_group_ids()

            if (not pq_group_id and not model_group_id):
                return Response(status_code=HTTP_404_NOT_FOUND)

            if (pq_group_id):
                self.grouplist.remove_group_by_id(group_id)
                self.print_queue()

            if (model_group_id):
                gr = self.journeys.get_group_by_id(group_id)
                for car in self.cars:
                    if car.id == gr.car_assigned.id:
                        car.deallocate(gr.people)
                        break

                # Call priority queue
                self.assign_cars_to_priority_groups()

                self.journeys.remove_group_by_id(group_id)

                self.print_queue()

        except:
            return Response(status_code=HTTP_400_BAD_REQUEST)

    def locate(self, group_id: int):

        """
            Aquí falta esto: 
            [x] 204 No Content When the group is waiting to be assigned to a car.

            [x] 404 Not Found When the group is not to be found.

            400 Bad Request When there is a failure in the request format or the
            payload can't be unmarshalled.
        """
        try:
            logging.info(f"IDS: {self.grouplist.get_group_ids()}")

            # Test if group id is in priorityqueue or is in journey
            pq_group_id :bool = group_id in self.grouplist.get_group_ids()
            model_group_id : bool = group_id in self.journeys.get_all_group_ids()

            if (pq_group_id):
                return Response(status_code=HTTP_204_NO_CONTENT)

            if (not pq_group_id or not model_group_id):
                return Response(status_code=HTTP_404_NOT_FOUND)

            # Buscar el coche asignado al grupo con el ID proporcionado
            for car in self.cars:
                if car.id == group_id:
                    return car
        except:
            return Response(status_code=HTTP_400_BAD_REQUEST)