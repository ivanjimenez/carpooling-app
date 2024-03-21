from fastapi import FastAPI, APIRouter, HTTPException, Query, status, BackgroundTasks, Response
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError, Field
from model import Car, Journey, Group
from typing import List, Any
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST
from starlette.requests import Request
import uvicorn
from logging_conf import setup as logging_conf
import logging
import random
import json

from CircularQueue import CircularQueue
from PriorityQueue import PriorityQueue

import asyncio


logging_conf()


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
        
        try:
            # if self.journeys.is_group_id_present(group["id"]):
            #     return Response(status_code=HTTP_400_BAD_REQUEST)
            grupo = Group(**group) # Convertivmos a model.group             
                
            for car in self.cars:
                if car.can_allocate(grupo.people):
                    # Start Journey
                    car.allocate(grupo.people)
                    grupo.car_assigned = car
                    self.journeys.add_group(grupo)
                    # self.grouplist.enqueue_with_priority(self.LOW_PRIORITY, grupo)
                    break
                
                else:
                    self.grouplist.enqueue_with_priority(self.LOW_PRIORITY, grupo)

                    break
             
           
            # if self.journeys.groups
            #     
            logging.info(f"Journeys: {self.journeys.groups}")
            logging.info(f"PriorityQueue: {self.grouplist._elements}")
            logging.info(f"Cars Avail: {self.cars}")
            

        except:
            logging.exception("An exception")
            raise HTTPException(status_code=400, detail="Bad Request")
        
        return Response(status_code=HTTP_200_OK)



    def drop_off():
        """
        1. Búsqueda por ID en la lista de grupos y verificar si está viajando, pues si no está viajando
        no tiene sentido borrarlo
        2. Si está viajando querrá decir que finalizamos viaje. Es decir, que liberamos los sitios del coche
        y borramos el grupo de personas.
        """
        
        pass


    def locate():
        """
        1. Devuelve coche del ID del grupo con el que esté viajando en formato json
        2. Si el grupo está esperando NOT FOUND
        """
        pass

    def getitem():
        item = grouplist.dequeue()
        print("Dequeued item:", item)

        print(grouplist._elements)

def init_app():
    
    App = Application()
    app = FastAPI(debug=True)
    
    @app.get('/')
    async def ready():
        return Response(status_code=HTTP_200_OK)
    
    # Adding cars Endpoint
    @app.put('/cars')
    async def add_cars(car_list: List[Car], req : Request):
        return App.add_cars(car_list, req)

    #Adding journey

    @app.post('/journey',status_code=HTTP_202_ACCEPTED)
    async def add_journey(group : dict):
        return App.add_journey(group)
    
    @app.post('/dropoff/{ID}')
    async def drop_off():
       return App.drop_off()

    @app.post('/locate/{ID}')
    async def locate():
       return App.locate()
    
    #Adding pop
    @app.post('/getitem')
    def get_item():
        return App.getitem()

    return app

    
