from pydantic import BaseModel


class Order(BaseModel):
    guig: str 
    date: str
    number: str

class OrderRes(BaseModel):
    order: Order


