from typing import Optional, List
from pydantic import BaseModel
from app.schemas.sche_product import ProductResponse  

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(CartItemBase):
    id: int
    cart_id: int
    product: Optional[ProductResponse] = None  
    class Config:
        orm_mode = True


class CartBase(BaseModel):
    user_id: int

class CartResponse(CartBase):
    id: int
    items: List[CartItemResponse] = [] 

    class Config:
        orm_mode = True