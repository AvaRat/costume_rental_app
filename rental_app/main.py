from typing import List
from datetime import date, timedelta
import secrets

import request

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

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

def redirect():
    request.post('https://enrollment-service.herokuapp.com/payu/notify', )

@app.post("/blik/notify")
async def notify(request: Request):
    logger_.info("got payment notify")
    body = await request.json()
    logger_.info(body)
    return JSONResponse(content={"message":"success"}, status_code=status.HTTP_200_OK)
