from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class OrderItem(BareBaseModel):
    __tablename__ = 'order_item'

    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False, default=0.0)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
