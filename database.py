from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

SQLALCHEMY_DATABASE_URL = "postgres://hlrafsvrnwrpfn:7c01a6b8f3277f8036c8f90f05110a7c7474976dad22a1112e9aa4b363469193@ec2-54-86-106-48.compute-1.amazonaws.com:5432/d8unk3o5k7s629"
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
