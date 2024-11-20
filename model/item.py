from pydantic import BaseModel, Field

class GetItemParams(BaseModel):
    query: str
    page: int | None = None
    limit: int | None = None

class Item(BaseModel):
    guid: str = Field(min_length=36)
    title:str
    code: str
    barcodes: list[str]


class ItemsRes(BaseModel):
    items: list[Item]
    total_pages: int = Field(..., alias='totalPages')
    total_items: int = Field(..., alias='totalItems')
    current_page: int = Field(..., alias='currentPage')
    items_per_page: int = Field(..., alias='itemsPerPage')
    start_item: int = Field(..., alias='startItem')
    end_item: int = Field(..., alias='endItem')


class ItemRes(BaseModel):
    item: Item

    