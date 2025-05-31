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
    #relationships
    agent = relationship("Agent", back_populates="connections")
    land_buyer = relationship("LandBuyer", back_populates="connections")

    @classmethod
    def create(cls, session, agent_id,  land_buyer_id):
        from .agent import Agent
        from .land_buyer import LandBuyer

        #validates that the agent exists
        agent = Agent.find_by_id(session, agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")
        
        #validates that the land_buyer exists
        land_buyer = LandBuyer.find_by_id(session, land_buyer_id)
        if not land_buyer:
            raise ValueError(f"Land buyer with ID {land_buyer_id} not found")
        
        #check if connection already
        existing = session.query(cls).filter_by(agent_id = agent_id, land_buyer_id = land_buyer_id).first()
        if existing:
            raise ValueError("This agent is already a land buyer connection")
        
        connection = cls(agent_id = agent_id, land_buyer_id = land_buyer_id)
        session.add(connection)
        session.commit()
        return connection    





        
