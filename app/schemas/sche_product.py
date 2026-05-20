from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    specifications: Optional[str] = None
    price: Optional[float] = 0.0
    inventory: Optional[int] = 0
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


class ProductCreateRequest(ProductBase):
    name: str
    price: float


class ProductUpdateRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]
    image_url: Optional[str]
    specifications: Optional[str]
    price: Optional[float]
    inventory: Optional[int]
    is_active: Optional[bool]


class ProductItemResponse(ProductBase):
    id: int
    name: str
    price: float
    inventory: int
    is_active: bool
    category: Optional[str]
    image_url: Optional[str]
    specifications: Optional[str]
