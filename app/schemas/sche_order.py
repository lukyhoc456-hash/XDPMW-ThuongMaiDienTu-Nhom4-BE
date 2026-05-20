from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.helpers.enums import OrderStatus


class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int


class OrderCreateRequest(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    shipping_address: Optional[str] = None
    notes: Optional[str] = None
    items: List[OrderItemRequest]


class OrderStatusRequest(BaseModel):
    status: OrderStatus


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    product_name: Optional[str] = None

    class Config:
        from_attributes = True


class OrderListItemResponse(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    customer_phone: Optional[str]
    status: str
    total_price: float
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class OrderDetailResponse(OrderListItemResponse):
    shipping_address: Optional[str]
    items: List[OrderItemResponse]
