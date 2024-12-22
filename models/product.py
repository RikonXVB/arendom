from sqlalchemy import Column, Integer, String, Float, Text
from config.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    subtitle = Column(String)
    price = Column(Float)
    image_url = Column(String)
    description = Column(Text)
    category = Column(String, index=True) 