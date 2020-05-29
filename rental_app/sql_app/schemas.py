from typing import List

from pydantic import BaseModel

class CostumeModel(BaseModel):
    name: str
    size: str
    type_: str
    collection: str
    price: float
    
    class Config:
        orm_mode = True