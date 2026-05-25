from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class Order(BareBaseModel):
    user_id = Column(Integer, nullable=True)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(20), nullable=True)
    shipping_address = Column(String(500), nullable=True)
    status = Column(String(50), default='pending')
    total_price = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    @property
    def items(self):
        return self.order_items
