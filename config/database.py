import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# URL для подключения к PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://restaurant_user:restaurant_pass@localhost:5432/restaurant_db")

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем движок и сессии
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    """Контекстный менеджер для работы с БД"""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()