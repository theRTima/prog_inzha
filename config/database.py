import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# Для trust-аутентификации нужно явно указать пустой пароль
DATABASE_URL = "postgresql://restaurant_user:restaurant_pass@localhost:5432/restaurant_db"

print(f"Подключаемся к: {DATABASE_URL}")

Base = declarative_base()

try:
    # connect_args может помочь с аутентификацией
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "application_name": "restaurant_app",
            # Явно указываем, что пароль не требуется
        }
    )
    
    # Тестируем подключение
    with engine.connect() as conn:
        print("✓ Успешное подключение к PostgreSQL")
        
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