from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.model_base import BareBaseModel


class Cart(BareBaseModel):
    __tablename__ = 'cart'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=True)
    session_id = Column(String(255), nullable=True, index=True)  # Cho guest users (không cần login)
    expires_at = Column(DateTime, nullable=True)  # Thời gian hết hạn của cart guest

    # Relationships
    user = relationship("User", back_populates="cart")
    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")