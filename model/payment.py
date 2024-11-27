from enum import Enum
from pydantic import BaseModel, Field


class PaymentQrCode(BaseModel):
    qr_code: str = Field(..., alias="qrCode")
    payment_url: str = Field(...,alias="paymentUrl")


class PaymentItems(BaseModel):
    uuid: str
    name: str
    count: int
    price: float
    amount: float
    description: str


class PaymentStatus(Enum):
    SUCCESS = 'success'
    PROCESSING = 'processing'
    FAIL = 'fail'


class PaymentRefund(BaseModel):
    uuid: str
    status: PaymentStatus
    amount: float
    items: PaymentItems


class PaymentInfo(BaseModel):
    uuid: str
    created_at: str = Field(...,alias="createdAt")
    status: PaymentStatus
    total_amount: float = Field(...,alias="totalAmount")
    payment_url: str = Field(...,alias="paymentUrl")
    refund: PaymentRefund
    items: PaymentItems


class PaymentInfoRes(BaseModel):
    payment_info: PaymentInfo