from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class Order(BareBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    shipping_address = Column(String(500), nullable=True)
    status = Column(String(50), default='pending')
    total_price = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)

    user = relationship("User", backref="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
