from typing import List
from datetime import datetime

from pydantic import BaseModel

class CostumeModel(BaseModel):
    name: str
    size: str
    type_: str
    collection: str
    price: float
    
    class Config:
        orm_mode = True

class ClientCreate(BaseModel):
    address:str
    phone_nr: str
    email: str
    login: str
    password: str

    class Config:
        orm_mode = True

class LocationPublic(BaseModel):
    address: str

    class Config:
        orm_mode = True

class CostumeModel(BaseModel):
    name: str
    size: str
    type_: str
    collection: str
    price: float

    class Config:
        orm_mode = True

class CostumeItem(BaseModel):
    id: int
    model: CostumeModel

    class Config:
        orm_mode = True

class ReservationBase(BaseModel):
    pick_up_date: datetime
    return_date: datetime
    pick_up_location_id: int

class ReservationCreate(ReservationBase):
    costumes: List[int] = [] #list of costume_id's

    class Config:
        orm_mode = True

class ReservationDb(ReservationBase):
    id: int
    date: datetime
    client_id: int
    
    class Config:
        orm_mode = True
