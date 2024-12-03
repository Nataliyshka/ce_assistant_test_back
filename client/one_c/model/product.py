from pydantic import BaseModel


class Product(BaseModel):
    product: str
    value: float
    state_id: float | None = None
