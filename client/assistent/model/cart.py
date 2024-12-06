from enum import Enum
from pydantic import BaseModel, Field


class PostCartStoreParams(BaseModel):
    store: str = Field(min_length=36)


class BonusProgram(BaseModel):
    guid: str
    name: str
    value: float


class CardType(Enum):
    GOLD = 'Золотая'
    SILVER = 'Железная'
    TREE = 'Деревянная'


class CountItemsReq(BaseModel):
    count: float
    

class Customer(BaseModel):
    name: str | None
    guid: str
    phone: str = Field(min_length=10)
    is_card_holder: bool = Field(..., alias="isCardholder")
    card_type: CardType | None = Field(..., alias="cardType")
    total_balance_bonuses: float = Field(..., alias="totalBalanceBonuses")
    total_availible_bonuses: float = Field(..., alias="totalAvailableBonuses")
    bonus_balance: list[BonusProgram] = Field(..., alias="bonusBalance")
    availible_bonuses: list[BonusProgram] = Field(..., alias="availableBonuses")


class Item(BaseModel):
    guid: str = Field(min_length=36)
    title: str
    code: str
    count: float
    sum: float
    discount_sum: float = Field(..., alias='discountSum')
    max_count: float = Field(..., alias='maxCount')
    total_accrual_bonuses: float = Field(..., alias='totalAccrualBonuses')
    accrual_bonuses: list[BonusProgram] = Field(..., alias='accrualBonuses')
    total_availible_bonuses: float | None = Field(..., alias='totalAvailableBonuses')
    availible_bonuses: list[BonusProgram] | None = Field(..., alias='availableBonuses')
    total_applied_bonuses: float = Field(..., alias='totalAppliedBonuses')
    applied_bonuses: list[BonusProgram] = Field(...,alias='appliedBonuses')


class CartStatus(Enum):
    OPEN = 'Open'
    SENDED = 'Sended'
    PAID = 'Paid'
    PROCESSING = 'Processing'
    CLOSED = 'Closed'


class Cart(BaseModel):
    uuid: str = Field(max_length=36)
    user: str = Field(max_length=36)
    customer: Customer | None
    store: str = Field(max_length=36)
    items: list[Item]
    modified: bool 
    total_count: float = Field(..., alias="totalCount")
    total: float
    total_sum: float = Field(..., alias="totalSum")
    total_discount_sum: float = Field(..., alias="totalDiscountSum")
    economy: float
    total_accrual_bonuses: float = Field(..., alias="totalAccrualBonuses")
    accrual_bonuses: list[BonusProgram] = Field(..., alias="accrualBonuses")
    total_applied_bonuses: float = Field(..., alias="totalAppliedBonuses")
    applied_bonuses: list[BonusProgram] = Field(..., alias="appliedBonuses") 
    status: CartStatus

class CartRes(BaseModel):
    cart: Cart


class OrderRes(BaseModel):
    order: str

