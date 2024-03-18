import model
from services import Service, GroupDoesNotExistError
from fastapi import FastAPI, APIRouter, HTTPException, Query, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError, Field
from schemas import Car, Group, Journey
from typing import List, Any
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED
import uvicorn
import sqlite3
import logging
from CircularQueue import CircularQueue

app = FastAPI()

@app.get('/')
async def ready():
    return { "service" : "success"}

@app.get('/cars')
async def cars(cars: List[Car]):
    for car in cars:
        return f"Success!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

