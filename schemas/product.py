from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    title: str
    subtitle: str
    price: float
    image_url: str
    description: Optional[str] = None
    category: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True 