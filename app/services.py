from priority_queue import PriorityQueue
from model import Car, Group, Journey

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

        try:
            self.cars = car_list

        except Exception:
            raise HTTPException(status_code=400, detail="Bad Request")

        self.print_queue()

        return Response(status_code=HTTP_200_OK)

    def add_journey(self, group : Group):


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
        logging.info(f"Journeys: {self.journeys}")
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
      
        """
        try:

            # Test if group id is in priorityqueue or is in journey
            pq_group_id :bool = group_id in self.grouplist.get_group_ids()
            model_group_id : bool = group_id in self.journeys.get_all_group_ids()
            
            # print(f" pq_group_id: {pq_group_id}, model_group_id: {model_group_id}")
            
            if (model_group_id):
                gr = self.journeys.get_group_by_id(group_id)
                for car in self.cars:
                    if car.id == gr.car_assigned.id:
                        car.deallocate(gr.people)
                        self.journeys.remove_group_by_id(group_id)
                                 
                        self.print_queue()
                        break
                # Call priority queue
                if (not self.grouplist.is_empty()):
                    self.assign_cars_to_priority_groups() 
                         
                return Response(status_code=HTTP_200_OK)

            if (not pq_group_id and not model_group_id):
                return Response(status_code=HTTP_404_NOT_FOUND)

            if (pq_group_id):
                self.grouplist.remove_group_by_id(group_id)
                self.print_queue()

           

        except:
            return Response(status_code=HTTP_400_BAD_REQUEST)

    def locate(self, group_id: int):

        """
   
        """
        try:
            logging.info(f"IDS: {self.grouplist.get_group_ids()}")

            # Test if group id is in priorityqueue or is in journey
            pq_group_id :bool = group_id in self.grouplist.get_group_ids()
            model_group_id : bool = group_id in self.journeys.get_all_group_ids()

            if model_group_id:
                 # Buscar el coche asignado al grupo con el ID proporcionado
                for group in self.journeys.groups:
                   
                    if group.id == group_id:
                        return {"id": group.id, "people": group.people}
                    
            if (pq_group_id):
                return Response(status_code=HTTP_204_NO_CONTENT)

            if (not pq_group_id and not model_group_id):
                return Response(status_code=HTTP_404_NOT_FOUND)

           
        except:
            return Response(status_code=HTTP_400_BAD_REQUEST)