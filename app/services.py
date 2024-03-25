from priority_queue import PriorityQueue
from model import Car, Group, Journey
from pydantic import ValidationError
from fastapi import HTTPException, Response
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_202_ACCEPTED

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
           # Validar cada objeto Car en la lista
            for car in car_list:
                Car(**car.dict())

        except ValidationError as ve:
            return Response(status_code=400)
        
        self.cars = car_list
        self.print_queue()
        return Response(status_code=HTTP_200_OK)

    def add_journey(self, group : Group):

        """
        Este método intenta asignar un grupo a un coche disponible.
        Si no hay coches disponibles, encola el grupo en la cola prioritaria.
        """
        try:
            group_model = Group(**group)
            
            # for journey in self.journeys.groups:
            #     journey.car_assigned.ca

            # Intentar asignar un coche disponible
            car_assigned = None
            for car in self.cars:
                if car.can_allocate(group_model.people):
                    car.allocate(group_model.people)
                    group_model.car_assigned = car
                    self.journeys.add_group(group_model)
                    logging.info("Group assigned to a car.")
                    self.print_queue()
                    return Response(status_code=HTTP_202_ACCEPTED)

            # Si no se asigna a un coche, encolar en la cola prioritaria
            self.grouplist.enqueue_with_priority(self.LOW_PRIORITY, group_model)
            logging.info("Group enqueued in priority queue.")
            self.print_queue()
            
            # Intentar asignar coches a grupos en la cola prioritaria
            self.assign_cars_to_priority_groups()

        except Exception as e:
            return Response(status_code=HTTP_400_BAD_REQUEST)



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
                    self.print_queue()
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
         Elimina el viaje por identificador
    
        :param group_id: id del grupo a elimienar
        :type group_id: int
       
        """
        
        # Test if group id is in priorityqueue or is in journey
        pq_group_id :bool = group_id in self.grouplist.get_group_ids()
        model_group_id : bool = group_id in self.journeys.get_all_group_ids()
        
        try:   
            
            # print(f" pq_group_id: {pq_group_id}, model_group_id: {model_group_id}")
            # If group exists in journeys, deallocate seats in Car
            
            if (model_group_id):
                gr = self.journeys.get_group_by_id(group_id)
                for car in self.cars:
                    if car.id == gr.car_assigned.id:
                        car.deallocate(gr.people)
                        self.journeys.remove_group_by_id(group_id)                    
                        self.print_queue()
                        break
                    
                # Call priority queue after drop the journey 
                if (not self.grouplist.is_empty()):
                    self.assign_cars_to_priority_groups() 
                         
                return Response(status_code=HTTP_200_OK)
            
            # En el caso que no esté en la lista de journeys y esté n PriorityQueue
            elif (pq_group_id):
                self.grouplist.remove_group_by_id(group_id)
                self.print_queue()
                return Response(status_code=HTTP_200_OK)
                
            else: # (not pq_group_id and not model_group_id):
                return Response(status_code=HTTP_404_NOT_FOUND)

            

        except Exception as e:
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