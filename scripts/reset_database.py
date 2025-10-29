import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import engine, Base
from sqlalchemy import text

def reset_database():
    try:
        # Импортируем модели из единого файла
        from models.models import MenuItem, Inventory, Recipe, Order, OrderItem
        
        # Принудительно удаляем все таблицы
        with engine.connect() as conn:
            conn.execute(text("SET session_replication_role = 'replica';"))
            
            conn.execute(text("DROP TABLE IF EXISTS order_items CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS orders CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS recipes CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS menu_items CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS inventory CASCADE"))
            
            conn.execute(text("SET session_replication_role = 'origin';"))
            conn.commit()

        print("tables deleted")
        
        Base.metadata.create_all(bind=engine)
        print("tables recreated")
        
        print("DB RECREATED")
    except Exception as e:
        print(f"error while creating DB: {e}")

if __name__ == "__main__":
    reset_database()
