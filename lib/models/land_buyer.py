from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class LandBuyer(Base):

    __tablename__ = "land_buyers"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(20), nullable=True)

    connections = relationship("Connection", back_populates="land_buyer", cascade="all, delete-orphan")