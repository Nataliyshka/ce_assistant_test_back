from pydantic import BaseModel


class ProductStock(BaseModel):
 product: str
 value: float
 state_id: float
