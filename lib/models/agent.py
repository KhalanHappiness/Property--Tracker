from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
import re

class Agent(Base):

    __tablename__ = "agents"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    license_number = Column(String(25), unique=True,nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)

    #relationships
    listings = relationship("Listing", back_populates="agent", cascade="all, delete-orphan")
    connections = relationship("Connection", back_populates="agent", cascade="all, delete-orphan")

    
    @property
    def full_info(self):
        return f"Id: {self.id}, Name:{self.name}, license_number:{self.license_number}, Email:{self.email}, Phone:{self.phone}"
    
    @property
    def listing_count(self):
        return len(self.listings)
    
    @property
    def connection_count(self):
        return len(self.connections)
    
    #input validation
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
    def create(cls, session, name, license_number, email, phone=None):
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if not license_number or len(license_number.strip()) < 2:
            raise ValueError("license number must be at least 2 characters long")
        
        if not cls.validate_email(email):
            raise ValueError("Invalid email format")
        
        if phone and not cls.validate_phone(phone):
            raise ValueError("Invalid phone format. Use XXX-XXX-XXXX, (XXX) XXX-XXXX, or XXXXXXXXXX")
        
        
        # Check if email already exists
        existing = session.query(cls).filter_by(email=email).first()
        if existing:
            raise ValueError("Email already exists")
        
        #check if license number already exists
        existing = session.query(cls).filter_by(license_number = license_number).first()
        if existing:
            raise ValueError("license number already exists")

        
        agent = cls(
            name=name.strip(),
            license_number = license_number.strip(),
            email=email.strip(),
            phone=phone,
            
        )
        session.add(agent)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    
        return agent
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, agent_id):
        return session.query(cls).filter_by(id=agent_id).first()
    
    @classmethod
    def find_by_name(cls, session, name):
       return session.query(cls).filter(cls.name.ilike(f"%{name}%")).all()
    
    def delete(self, session):
        session.delete(self)
        session.commit()

    def __repr__ (self):
        return f"Agent(id={self.id}, name={self.name}, license= {self.license_number}, email={self.email})"
    

 
    
    

    
