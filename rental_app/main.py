from typing import List
from datetime import date, timedelta
import secrets

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status
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

@app.post("/payment/notify")
def notify():
    logger_.info("got payment notify")
    return JSONResponse(content={"message":"success"}, status_code=status.HTTP_200_OK)
