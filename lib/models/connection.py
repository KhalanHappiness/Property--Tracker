from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base 

class Connection(Base):

    __tablename__ = "connections"


    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    land_buyer_id = Column(Integer, ForeignKey('land_buyers.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())

    agent = relationship("Agent", back_populates="connections")
    land_buyer = relationship("LandBuyer", back_populates="connections")




        
