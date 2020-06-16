from typing import List, OrderedDict
from datetime import datetime

from pydantic import BaseModel

class CostumeModelBase(BaseModel):
    name: str
    size: str
    type: str
    collection: str
    
    class Config:
        orm_mode = True

class CostumeModelCreate(CostumeModelBase):

    class Config:
        orm_mode = True

class CostumeModelDb(CostumeModelBase):
    id: int
    price: float

    class Config:
        orm_mode = True

class CostumeModelOut(CostumeModelBase):
    model_id:int

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

class ClientBase(BaseModel):
    id: int
    address:str
    phone_nr: str
    email: str
    login: str
    password: str
    nr_reservations: int

    class Config:
        orm_mode = True

class LocationPublic(BaseModel):
    address: str
    name: str

    class Config:
        orm_mode = True


class CostumeItem(BaseModel):
    id: int
    model: CostumeModelDb

    class Config:
        orm_mode = True

class CostumeItemOut(BaseModel):
    model: CostumeModelOut
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

class ReservationCreateTest(ReservationBase):
    costume_ids: List[int] = []
    class Config:
        orm_mode=True

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

class ReservationOut(BaseModel):
    reservation_code: int
    date: datetime
    pick_up_date: datetime
    return_date: datetime
    pick_up_address: LocationPublic
    costumes: List[CostumeItemOut]
    total_cost: float

    class Config:
        orm_mode=True