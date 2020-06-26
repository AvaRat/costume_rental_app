from typing import List, OrderedDict
from datetime import date

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

class LocationBase(BaseModel):
    address: str
    name: str

    class Config:
        orm_mode = True 

class LocationDB(LocationBase):
    id: int

    class Config:
        orm_mode = True


class CostumeItem(BaseModel):
    id: int
    model: CostumeModelDb

    class Config:
        orm_mode = True

class CostumeItemOut(BaseModel):
    model: CostumeModelOut
    quantity: int

    class Config:
        orm_mode = True

class CostumeItemSystem(CostumeItem):
    location: LocationDB

    class Config:
        orm_mode = True

class CostumeModelAmount(BaseModel):
    model_id: int
    quantity: int


class ReservationBase(BaseModel):
    pick_up_date: date
    return_date: date
    pick_up_location_id: int

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
    class Config:
        orm_mode = True;

class ReservationDb(ReservationBase):
    id: int
    date: date
    client_id: int
    valid: bool
    
    class Config:
        orm_mode = True

class ReservationOut(BaseModel):
    reservation_code: int
    date: date
    pick_up_date: date
    return_date: date
    pick_up_address: LocationBase
    costumes: List[CostumeItemOut]
    total_cost: float

    class Config:
        orm_mode=True

class RentalBase(BaseModel):
    start_date: date
    end_date: date
    class Config:
        orm_mode=True   

class RentalDb(RentalBase):
    id: str
    reservation_id: str
    class Config:
        orm_mode=True

class RentalOut(RentalBase):
    costumes: List[CostumeItemOut]
    total_cost: float

    class Config:
        orm_mode=True