from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Agent(Base):

    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    lisense_number = Column(String(25), nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(20), nullable=True)

    listings = relationship("Listing", back_populates="agent", cascade="all, delete-orphan")
    connections = relationship("Connection", back_populates="agent", cascade="all, delete-orphan")