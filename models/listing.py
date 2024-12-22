from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    location = Column(String)
    category = Column(String)
    contact = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    image_url = Column(String)

    images = relationship("ListingImage", back_populates="listing")
    favorites = relationship("Favorite", back_populates="listing")

class ListingImage(Base):
    __tablename__ = "listing_images"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    image_url = Column(String)
    image_data = Column(LargeBinary)
    content_type = Column(String)

    listing = relationship("Listing", back_populates="images")