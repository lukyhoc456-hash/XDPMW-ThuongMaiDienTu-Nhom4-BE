from sqlalchemy import Column, String, Boolean, DateTime

from app.models.model_base import BareBaseModel


class User(BareBaseModel):
    full_name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(50), default='guest')
    last_login = Column(DateTime)
