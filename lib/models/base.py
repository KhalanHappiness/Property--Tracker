from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///property_management.db"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()