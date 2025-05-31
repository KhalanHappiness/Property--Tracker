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

    @property
    def full_info(self):
        """Returns basic connection information"""
        agent_name = self.agent.name if self.agent else f"Agent ID: {self.agent_id}"
        buyer_name = self.land_buyer.name if self.land_buyer else f"Buyer ID: {self.land_buyer_id}"
        created = self.created_at.strftime('%Y-%m-%d') if self.created_at else 'Unknown'
        
        return f"Connection #{self.id}: {agent_name} ↔ {buyer_name} (Created: {created})"

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
        
        #check if connection already exists
        existing = session.query(cls).filter_by(agent_id = agent_id, land_buyer_id = land_buyer_id).first()
        if existing:
            raise ValueError("This agent is already a land buyer connection")
        
        connection = cls(agent_id = agent_id, land_buyer_id = land_buyer_id)
        session.add(connection)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return connection 
    
    @classmethod   
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, connection_id):
        return session.query(cls).filter_by(id = connection_id).first()
    
    @classmethod
    def find_by_agent_id(cls, session, agent_id):
        return session.query(cls).filter_by(agent_id=agent_id).all()

    @classmethod
    def find_by_land_buyer_id(cls, session, land_buyer_id):
        return session.query(cls).filter_by(land_buyer_id=land_buyer_id).all()
    
    def delete(self,session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f"Connection( id= {self.id}, agent_id={self.agent_id}, land_buyer_id = {self.land_buyer_id} )"





        
