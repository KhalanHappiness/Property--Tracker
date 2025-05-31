from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
import re

class Agent(Base):

    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    lisense_number = Column(String(25), unique=True,nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(20), nullable=True)

    #relationships
    listings = relationship("Listing", back_populates="agent", cascade="all, delete-orphan")
    connections = relationship("Connection", back_populates="agent", cascade="all, delete-orphan")

    #input validation
    @property
    def full_info(self):
        return f"Id: {self.id,}, Name:{self.name}, lisense_number:{self.lisense_number}, Email:{self.email}, Phone:{self.phone}"
    
    @property
    def listing_count(self):
        return len(self.listings)
    
    @property
    def connection_count(self):
        return len(self.connections)
    
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        if not phone:
            return True  # Phone is optional
        pattern = r'^\d{3}-\d{3}-\d{4}$|^\(\d{3}\)\s*\d{3}-\d{4}$|^\d{10}$'
        return re.match(pattern, phone) is not None
    
    @classmethod
    def create(cls, session, name, lisence_number, email, phone=None):
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if not lisence_number or len(lisence_number.strip()) < 2:
            raise ValueError("lisense number must be at least 2 characters long")
        
        if not cls.validate_email(email):
            raise ValueError("Invalid email format")
        
        
        # Check if email already exists
        existing = session.query(cls).filter_by(email=email).first()
        if existing:
            raise ValueError("Email already exists")
        
        #check if lisense number already exists
        existing = session.query(cls).filter_by(lisence_number = lisence_number).first()
        if existing:
            raise ValueError("lisence number already exists")

        
        agent = cls(
            name=name.strip(),
            lisence_number = lisence_number.strip(),
            email=email.strip(),
            phone=phone,
            
        )
        session.add(agent)
        session.commit()
        return agent
    
    

    
