import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

DATABASE_URL = "postgresql://restaurant_user:restaurant_pass@localhost:5434/restaurant_db"

Base = declarative_base()

try:
    engine = create_engine(DATABASE_URL)
    
    def init_database():
        from models.models import MenuItem, Inventory, Recipe, Order, OrderItem
        
        Base.metadata.create_all(bind=engine)
        print("DB INITED")
    
    with engine.connect() as conn:
        print("connected to PostgreSQL")
        init_database()
        
except Exception as e:
    print(f"error: {e}")
    exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
