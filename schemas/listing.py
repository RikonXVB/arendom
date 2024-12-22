from pydantic import BaseModel
from typing import List
from datetime import datetime

class ListingBase(BaseModel):
    title: str
    category: str
    description: str
    price: float
    location: str
    contact: str

    model_config = {
        "from_attributes": True
    }

class ListingCreate(ListingBase):
    pass

class ListingImage(BaseModel):
    id: int
    content_type: str

    model_config = {
        "from_attributes": True
    }

class Listing(ListingBase):
    id: int
    created_at: datetime
    images: List[ListingImage] = []

    model_config = {
        "from_attributes": True
    }