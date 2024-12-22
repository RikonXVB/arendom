from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), index=True)

    # Отношение к модели Listing
    listing = relationship("Listing", back_populates="favorites") 