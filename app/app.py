from fastapi import FastAPI, APIRouter, BackgroundTasks, Response, Form
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError, Field
from services import Application
from model import Car
from typing import List
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED
from starlette.requests import Request
from logging_conf import setup as logging_conf
import random
import json

import asyncio


def init_app():
    
    Service = Application()
    app = FastAPI(debug=True)
    
    logging_conf()
    
    @app.get('/')
    def ready():
        return Response(status_code=HTTP_200_OK)
    
    # Adding cars Endpoint
    @app.put('/cars')
    async def add_cars(car_list: List[Car], req : Request):
        return Service.add_cars(car_list, req)

    #Adding journey

    @app.post('/journey',status_code=HTTP_202_ACCEPTED)
    async def add_journey(group : dict):
        return Service.add_journey(group)
    
    @app.post('/dropoff', status_code=HTTP_200_OK)
    async def drop_off(group_id: int = Form(...)):
       return Service.drop_off(group_id)

    # Agregar endpoint para localizar un coche por ID de grupo
    @app.post('/locate', status_code=HTTP_200_OK)
    async def locate(group_id: int = Form(...)):
        return Service.locate(group_id)

    return app

    
