from typing import List, OrderedDict
from datetime import datetime

from pydantic import BaseModel

class CostumeModel(BaseModel):
    id: str
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
    name: str

    class Config:
        orm_mode = True


class CostumeItem(BaseModel):
    id: int
    model: CostumeModel

    class Config:
        orm_mode = True

class CostumeItemOut(BaseModel):
    model_id: int
    model: CostumeModel
    location: LocationPublic
    n_items: int

    class Config:
        orm_mode = True

class CostumeItemSystem(CostumeItem):
    location: LocationPublic

    class Config:
        orm_mode = True
    

class ReservationBase(BaseModel):
    pick_up_date: datetime
    return_date: datetime
    pick_up_location_id: int

class CostumeModelAmount(BaseModel):
    model_id: int
    quantity: int

class ReservationCreate(ReservationBase):
    costumes: List[CostumeModelAmount] = [] #dict of

    class Config:
        orm_mode = True

class ReservationModify(ReservationBase):
    id: int
    cancel: bool
    class Config:
        orm_mode = True;

class ReservationDb(ReservationBase):
    id: int
    date: datetime
    client_id: int
    
    class Config:
        orm_mode = True

class ReservationOut(ReservationBase):
    id: int
    date: datetime
    costumes: List[CostumeModel]
    total_cost: float

    class Config:
        orm_mode=True