from pydantic import BaseModel, Field

class Coordinates(BaseModel):
    lat: float
    lon: float


class Store(BaseModel):
    guid: str = Field(min_length=36)
    name: str
    address: str
    division: str = Field(min_length=36)
    coordinates: Coordinates


class StoresRes(BaseModel):
    stores: list[Store]


class StoreRes(BaseModel):
    store: Store
    

