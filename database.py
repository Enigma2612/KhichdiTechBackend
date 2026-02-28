# database.py - Neon Postgres connection template with SQLAlchemy ORM for your tables
# Install: pip install sqlalchemy psycopg[binary] python-dotenv alembic (optional for migrations)

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Neon connection string from .env: DATABASE_URL="postgresql://user:pass@host/db?sslmode=require"
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Set DATABASE_URL in .env file from Neon console")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)  # Handles Neon's scale-to-zero
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Table Models (adjust fields as needed for your use case)
class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    role = Column(String(100), unique=True)

class Items(Base):
    __tablename__ = "Items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(500))

# Users.items = relationship("Items", order_by=Items.id, back_populates="users")

class Inventory(Base):
    __tablename__ = "Inventory"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("Items.id"))
    user_id = Column(Integer, ForeignKey("Users.id"))
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    items = relationship("Items")
    users = relationship("Users")

class Transit(Base):
    __tablename__ = "Transit"
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("Inventory.id"))
    from_location = Column(String(100))
    to_location = Column(String(100))
    status = Column(String(50), default="in_transit")
    started_at = Column(DateTime, default=func.now())
    inventory = relationship("Inventory")

# Create tables
Base.metadata.create_all(bind=engine)

# Usage example
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test connection and create tables
if __name__ == "__main__":
    from sqlalchemy import text
    with SessionLocal() as session:
        result = session.execute(text("SELECT version()"))
        print("Connected:", result.scalar())
    print("Tables ready: Users, Items, Inventory, Transit")
