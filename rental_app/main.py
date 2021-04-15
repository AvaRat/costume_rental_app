from typing import List
from datetime import date, timedelta
import secrets

import requests

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from .sql_app import crud, models, schemas

origins = [
    'http://localhost:8080',
    'http://127.0.0.1'
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger_ = logging.getLogger('uvicorn.info')

def redirect(data):
    response = requests.post('https://enrollment-service.herokuapp.com/payment/payu/blik/notify', json=data)
    logger_.info(response.status_code)

@app.post("/blik/notify")
async def notify(request: Request):
    logger_.info("got payment notify")
    body = await request.json()
    logger_.info(body)
    redirect(body)
    return JSONResponse(content={"message":"success"}, status_code=status.HTTP_200_OK)


@app.get("/models")
def get_all_models():
    all_models = {'name':'Bawarczyk', 'collection':'dookoła świata','size':'M'}
    return all_models


    