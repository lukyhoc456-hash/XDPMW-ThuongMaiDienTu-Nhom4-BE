from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    price: float
    inventory: Optional[int] = 0
    is_active: Optional[bool] = True
    image_url: Optional[str] = None
    specifications: Optional[dict] = None



class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
