from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import re
from .base import Base

class LandBuyer(Base):

    __tablename__ = "land_buyers"

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(20), nullable=True)

    #Relationship
    connections = relationship("Connection", back_populates="land_buyer", cascade="all, delete-orphan")

    @property
    def buyer_info(self):
        return f"Id: {self.id}, Name: {self.name}, Email:{self.email}, Phone:{self.phone or 'N/A'}"
    
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
    def create(cls, session, name, email, phone=None):
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        
        if not cls.validate_email(email):
            raise ValueError("Invalid email format")
        
        if phone and not cls.validate_phone(phone):
            raise ValueError("Invalid phone format. Use XXX-XXX-XXXX, (XXX) XXX-XXXX, or XXXXXXXXXX")
        
        # Check if email already exists
        existing = session.query(cls).filter_by(email=email).first()
        if existing:
            raise ValueError("Email already exists")
        
        land_buyer = cls(name=name.strip(), email=email.strip(), phone=phone)
        session.add(land_buyer)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        return land_buyer
    
   
    @classmethod
    def update_by_id(cls, session, landbuyer_id, name=None, email=None, phone=None):
        
        land_buyer = cls.find_by_id(session, landbuyer_id)
        if not land_buyer:
            raise ValueError(f"Land buyer with ID {landbuyer_id} not found")
        
        # Validate name if provided
        if name is not None:
            if not name or len(name.strip()) < 2:
                raise ValueError("Name must be at least 2 characters long")
        
        # Validate email if provided
        if email is not None:
            if not cls.validate_email(email):
                raise ValueError("Invalid email format")
            
            # Check if email already exists (excluding current land buyer)
            existing = session.query(cls).filter(
                cls.email == email.strip(),
                cls.id != land_buyer.id
            ).first()
            if existing:
                raise ValueError("Email already exists")
        
        # Validate phone if provided
        if phone is not None and phone and not cls.validate_phone(phone):
            raise ValueError("Invalid phone format. Use XXX-XXX-XXXX, (XXX) XXX-XXXX, or XXXXXXXXXX")
        
        # Update fields if provided
        if name is not None:
            land_buyer.name = name.strip()
        if email is not None:
            land_buyer.email = email.strip()
        if phone is not None:
            land_buyer.phone = phone
        
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        
        return land_buyer       
    

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, landbuyer_id):
        return session.query(cls).filter_by(id = landbuyer_id).first()
    @classmethod
    def find_by_email(cls, session, input_email):
        return session.query(cls).filter_by(email=input_email).first()
    
    def delete(self, session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f"LandBuyer(id={self.id}, name={self.name}, email={self.email})"
    
    

    