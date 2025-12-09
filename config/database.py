import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from typing import Generator

# Конфигурация через переменные окружения
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://restaurant_user:restaurant_pass@localhost:5434/restaurant_db"
)

Base = declarative_base()
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database() -> None:
    """Создает все таблицы в базе данных."""
    Base.metadata.create_all(bind=engine)

def drop_database() -> None:
    """Удаляет все таблицы из базы данных."""
    Base.metadata.drop_all(bind=engine)

def verify_connection() -> bool:
    """Проверяет подключение к базе данных."""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False

@contextmanager
def get_db() -> Generator:
    """Контекстный менеджер для получения сессии БД."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()