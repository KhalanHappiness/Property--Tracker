from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Listing(Base):

    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer,ForeignKey('agents.id'), nullable=False)
    address = Column(String(100), nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    size = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)

    agent = relationship("Agent", back_populates="listings")

    @property
    def full_info(self):
        price_str = f"${self.price}" if self.price else "Price TBD"
        status = "Available" if self.is_available else "Unavailable"
        return f"Id: {self.id}, address: {self.address}, Price: {price_str}, Status: {status}, Agent: {self.agent.name}"
    
    @staticmethod
    def validate_price(price):
        if price is None:
            return True
        try:
            price_float = float(price)
            return price_float >= 0
        except (ValueError, TypeError):
            return False
        
    @classmethod
    def create(cls, session, agent_id, address, size, price=None, description=None, is_available=True):
        from .agent import Agent
        if not address or len(address.strip()) < 5:
            raise ValueError("address must be at least 5 characters long")
        
        # Validate agent exists
        agent = Agent.find_by_id(session, agent_id)
        if not agent:
            raise ValueError(f"agent with ID {agent_id} not found")
        
        if price is not None and not cls.validate_price(price):
            raise ValueError("Price must be a positive number")
        
        listing = cls(
            agent_id=agent_id,
            address=address.strip(),
            price=float(price) if price is not None else None,
            size = size,
            description = description,
            is_available=bool(is_available)
        )
        session.add(listing)
        session.commit()
        return listing
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, listing_id):
        return session.query(cls).filter_by(id = listing_id).first()
    
    @classmethod
    def find_by_agent(cls, session, agent_id):
        return session.query(cls).filter_by(agent_id = agent_id).all()
    
    def delete(self, session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f"Listing(id = {self.id}, address={self.address}, price={self.price})"
        

