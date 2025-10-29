import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import engine, Base
from sqlalchemy import text

def reset_database():
    try:
        # Принудительно удаляем все таблицы в правильном порядке (из-за внешних ключей)
        with engine.connect() as conn:
            # Временно отключаем проверку внешних ключей
            conn.execute(text("SET session_replication_role = 'replica';"))
            
            # Удаляем таблицы в правильном порядке зависимостей
            conn.execute(text("DROP TABLE IF EXISTS order_items CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS orders CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS recipes CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS menu_items CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS inventory CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS menu CASCADE"))  # На случай если старая таблица осталась
            
            # Включаем проверку внешних ключей обратно
            conn.execute(text("SET session_replication_role = 'origin';"))
            conn.commit()

        print("Таблицы удалены")

        # Импортируем модели внутри функции
        from models.order_model import Order, OrderItem
        from models.menu_model import MenuItem
        from models.inventory_model import Inventory
        from models.recipe_model import Recipe
        
        Base.metadata.create_all(bind=engine)
        print("Таблицы созданы заново")
        
        print("База данных успешно пересоздана")
    except Exception as e:
        print(f"Ошибка при пересоздании БД: {e}")

if __name__ == "__main__":
    reset_database()