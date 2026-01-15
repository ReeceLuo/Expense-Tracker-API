from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# Define application settings
class Settings(BaseSettings):
    database_url: str
    secret_key: str
    model_config = {"env_file": ".env"}

# Load settings
settings = Settings()

# Create engine
engine = create_engine(
    settings.database_url,
    echo=True
)

# Create SessionMaker
SessionLocal = sessionmaker(
    bind=engine,
    autocommit = False,
    autoflush = False
)

# Instantiate declarative base for sqlalchemy models to inherit from
DeclarativeBase = declarative_base()

# Dependency function to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

