from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Listing(Base):

    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer,ForeignKey('agents.id'), nullable=False)
    address = Column(String(25), nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    size = Column(String(20), nullable=True)
    description = Column(String(50), nullable=True)

    agent = relationship("Agent", back_populates="listings")

