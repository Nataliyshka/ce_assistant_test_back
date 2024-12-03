from pydantic import BaseModel


class Order(BaseModel):
    guid: str 
    date: str
    number: str