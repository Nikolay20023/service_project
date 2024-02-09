from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ServiceDB(BaseModel):
    name: str
    discription: str


class ServiceCreate(ServiceDB):
    price: int


class ServiceUpdate(ServiceCreate):
    pass
