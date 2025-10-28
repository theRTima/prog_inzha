import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.menu_model import MenuItem
from models.inventory_model import Inventory
from models.order_model import Order, OrderItem
from sqlalchemy.sql import text

def seed_database():
    db = SessionLocal()
    
    try:
        # Очищаем таблицы
        db.execute(text("DELETE FROM order_items"))
        db.execute(text("DELETE FROM orders"))
        db.execute(text("DELETE FROM menu"))
        db.execute(text("DELETE FROM inventory"))
        
        # Добавляем тестовое меню
        menu_items = [
            MenuItem(name="Стейк Рибай", category="Горячие блюда", price=1200.00, available=True, description="Стейк с картофелем"),
            MenuItem(name="Цезарь с курицей", category="Салаты", price=450.00, available=True, description="Салат Цезарь с куриной грудкой"),
            MenuItem(name="Томатный суп", category="Супы", price=350.00, available=True, description="Томатный суп с базиликом"),
            MenuItem(name="Тирамису", category="Десерты", price=400.00, available=False, description="Классический тирамису"),
            MenuItem(name="Кофе латте", category="Напитки", price=250.00, available=True, description="Кофе латте 300 мл"),
        ]
        
        for item in menu_items:
            db.add(item)
        
        # Добавляем тестовые заказы
        orders = [
            Order(customer_name="Иван Петров", phone="+7 (912) 345-67-89", status="Новый", total=2500),
            Order(customer_name="Мария Сидорова", phone="+7 (923) 456-78-90", status="Готовится", total=1800),
            Order(customer_name="Алексей Иванов", phone="+7 (934) 567-89-01", status="Готов к выдаче", total=3200),
        ]
        
        for order in orders:
            db.add(order)
        
        db.commit()
        print("Тестовые данные успешно добавлены")
        
    except Exception as e:
        print(f"Ошибка при добавлении тестовых данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()