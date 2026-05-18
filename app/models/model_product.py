from sqlalchemy import Column, String, Float, Integer, Boolean, Text, JSON
from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class Product(BareBaseModel):
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    inventory = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    image_url = Column(String(500), nullable=True)
    specifications = Column(JSON, nullable=True)

    order_items = relationship("OrderItem", back_populates="product")
