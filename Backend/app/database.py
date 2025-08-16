from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv('DB_URL')
print(DATABASE_URL)

if not DATABASE_URL:
	raise ValueError("Environment variable 'DB_URL' is not set or is empty.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
