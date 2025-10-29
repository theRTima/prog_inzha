import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

DATABASE_URL = "postgresql://restaurant_user:restaurant_pass@localhost:5433/restaurant_db"

Base = declarative_base()

try:
    engine = create_engine(DATABASE_URL)
    
    def init_database():
        """Безопасная инициализация БД с отложенным импортом моделей"""
        # Импортируем модели внутри функции чтобы избежать циклических импортов
        from models.order_model import Order, OrderItem
        from models.menu_model import MenuItem
        from models.inventory_model import Inventory
        from models.recipe_model import Recipe
        
        Base.metadata.create_all(bind=engine)
        print("✓ Таблицы БД инициализированы")
    
    # Проверяем подключение
    with engine.connect() as conn:
        print("✓ Успешное подключение к PostgreSQL")
        init_database()
        
except Exception as e:
    print(f"✗ Ошибка подключения: {e}")
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