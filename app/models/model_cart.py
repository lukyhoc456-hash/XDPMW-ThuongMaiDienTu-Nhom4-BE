from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class Cart(BareBaseModel):
    __tablename__ = 'cart'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=True)
    session_id = Column(String(255), nullable=True, index=True)
    expires_at = Column(DateTime, nullable=True)

    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    user = relationship("User", back_populates="cart")