import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import engine, Base
from models.order_model import Order
from models.menu_model import MenuItem
from models.inventory_model import Inventory
from models.recipe_model import Recipe

def reset_database():
    # Удаляем все таблицы
    Base.metadata.drop_all(bind=engine)
    
    # Создаем таблицы заново
    Base.metadata.create_all(bind=engine)
    print("База данных пересоздана")

if __name__ == "__main__":
    reset_database()