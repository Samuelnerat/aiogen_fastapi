from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0123456789@localhost/aiogen"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base= declarative_base()

# Dependency 
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()