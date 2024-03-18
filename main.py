from fastapi import FastAPI, APIRouter, HTTPException, Query, status, BackgroundTasks
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError, Field
from model import Car, Journey, Group
from typing import List, Any
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED
import uvicorn
import sqlite3
import logging
import queue
from CircularQueue import CircularQueue
from PriorityQueue import PriorityQueue

logger = logging.getLogger()
FORMAT = '%(levelname)s: %(asctime)s -> %(message)s'
logging.basicConfig(format=FORMAT)

app = FastAPI(debug=True)

# Global variables to store car data and journey information

journeys = []
cars = CircularQueue()

grouplist = PriorityQueue()

@app.get('/')
async def ready():
    return { "service" : "ready"}


#Adding journey

@app.post('/journey',status_code=HTTP_202_ACCEPTED)
async def add_journey(group : dict):
    global grouplist

     # Comprobación básica de la estructura del JSON
    if "id" not in group or "people" not in group:
        raise HTTPException(status_code=400, detail="Bad Request")

    if group["id"] < 1 or not (1 <= group["people"] <= 6):
        raise HTTPException(status_code=400, detail="Bad Request")

    grouplist.insert(group , 1)
    grouplist.print_elements()
    return {"GroupAdded": "Ok"}

# Adding cars Endpoint
@app.put('/cars')
async def reset_and_add_cars(car_list: List[Car]):
    global cars
    
    cars.reset()
    
    for car in car_list:
        if car.id < 1 or not (4 <= car.seats <= 6):
            raise HTTPException(status_code=400, detail="Bad Request")
        
    for car in car_list:
        cars.add_item(car)
        logger.warning("Car created!")
 
    print(f"Cars Queue: {cars.list}")
        
   
            
    return {"output" : "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
