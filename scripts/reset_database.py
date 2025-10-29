import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import engine, Base

def reset_database():
    try:
        # Импортируем модели внутри функции
        from models.order_model import Order, OrderItem
        from models.menu_model import MenuItem
        from models.inventory_model import Inventory
        from models.recipe_model import Recipe
        
        Base.metadata.drop_all(bind=engine)
        print("Таблицы удалены")
        
        Base.metadata.create_all(bind=engine)
        print("Таблицы созданы заново")
        
        print("База данных успешно пересоздана")
    except Exception as e:
        print(f"Ошибка при пересоздании БД: {e}")

if __name__ == "__main__":
    reset_database()