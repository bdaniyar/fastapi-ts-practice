from sqlalchemy.orm import relationship
from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from fastapi_tasks_db.databasework.database import Base

class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer,primary_key=True)
    name= Column(String, nullable=False)
    location= Column(String, nullable=False)
    services= Column(JSON)
    rooms_quantity= Column(Integer, nullable=False)
    image_id= Column(Integer)
    rooms = relationship("Rooms", back_populates="hotel")

class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer,primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)
    hotel = relationship("Hotels", back_populates="rooms")