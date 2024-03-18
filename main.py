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
from ListaCircular import ListaCircular
from PriorityQueue import PriorityQueue

logger = logging.getLogger()
FORMAT = '%(levelname)s: %(asctime)s -> %(message)s'
logging.basicConfig(format=FORMAT)

app = FastAPI(debug=True)

# Global variables to store car data and journey information

journeys = []
cars = ListaCircular()

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
    car_tuple : tuple
    
    for car in car_list:
        if car.id < 1 or not (4 <= car.seats <= 6):
            raise HTTPException(status_code=400, detail="Bad Request")
  
    try:
        sqlite3conn = sqlite3.connect(':memory:')
        cursor = sqlite3conn.cursor()
        
        sqlite_create_car_table_query = '''CREATE TABLE IF NOT EXISTS CAR (
                                    id INTEGER PRIMARY KEY,
                                    seats INTEGER NOT NULL,
                                    empty_seats INTEGER NOT NULL);'''
        
        cursor.execute(sqlite_create_car_table_query)
        sqlite3conn.commit()
        logger.warning("sqlite3 CAR created!")
        
        # Adding a Car
        sql_add_car = "INSERT INTO CAR VALUES (?,?,?)"
        
        for car in car_list:
            car_tuple = (car.id, car.seats, car.seats)
            cursor.execute(sql_add_car, car_tuple)
            cars.agregar_elemento(car_tuple)
            sqlite3conn.commit()
            logger.warning("Car created!")
        
        sql_sel = "SELECT * FROM CAR"
        cursor.execute(sql_sel)
        carsbd = cursor.fetchall()
        logger.warning(f"Cars created: {carsbd}")
        logger.warning(f"Circurlar List Cars created:{cars.lista}")
        cursor.close()
        
    except sqlite3.Error as e:
        logger.warning(f"Error while creating table: {e}")
    
    finally:
        
        if (sqlite3conn):
            sqlite3conn.close()
            logger.warning("In Memory DB closed!")
            
    return {"output" : "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
