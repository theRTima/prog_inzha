import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.models import MenuItem, Inventory, Recipe, Order, OrderItem  # Обновленный импорт
from sqlalchemy.sql import text

def seed_database():
    db = SessionLocal()
    
    try:
        # Очищаем таблицы в правильном порядке
        db.execute(text("DELETE FROM order_items"))
        db.execute(text("DELETE FROM orders"))
        db.execute(text("DELETE FROM recipes"))
        db.execute(text("DELETE FROM menu_items"))
        db.execute(text("DELETE FROM inventory"))
        
        db.commit()
        print("✓ Старые данные очищены")
        
        # Добавляем тестовые данные (код без изменений)
        menu_items = [MenuItem(name="Стейк Рибай", category="Горячие блюда", price=1200.00, available=True, description="Стейк с картофелем"),
            MenuItem(name="Цезарь с курицей", category="Салаты", price=450.00, available=True, description="Салат Цезарь с куриной грудкой"),
            MenuItem(name="Томатный суп", category="Супы", price=350.00, available=True, description="Томатный суп с базиликом"),
            MenuItem(name="Тирамису", category="Десерты", price=400.00, available=True, description="Классический тирамису"),
            MenuItem(name="Кофе латте", category="Напитки", price=250.00, available=True, description="Кофе латте 300 мл"),
            MenuItem(name="Бургер", category="Горячие блюда", price=600.00, available=True, description="Бургер с говядиной"),
            MenuItem(name="Греческий салат", category="Салаты", price=380.00, available=True, description="Греческий салат с оливковым маслом"),
        ]
        
        for item in menu_items:
            db.add(item)
        
        db.commit()
        print("menu added")
        
        inventory_items = [Inventory(name="Говядина", category="Мясо", unit="кг", current_stock=15.5, min_stock=5.0, supplier="Мясной двор"),
            Inventory(name="Куриное филе", category="Мясо", unit="кг", current_stock=8.2, min_stock=3.0, supplier="Птицефабрика"),
            Inventory(name="Помидоры", category="Овощи", unit="кг", current_stock=12.0, min_stock=4.0, supplier="Овощная база"),
            Inventory(name="Сыр пармезан", category="Молочные", unit="кг", current_stock=2.5, min_stock=1.0, supplier="Сыроварня"),
            Inventory(name="Кофе зерновой", category="Бакалея", unit="кг", current_stock=5.0, min_stock=2.0, supplier="Кофейная компания"),
            Inventory(name="Салат Айсберг", category="Овощи", unit="кг", current_stock=3.2, min_stock=2.0, supplier="Овощная база"),
            Inventory(name="Хлебные булочки", category="Бакалея", unit="шт", current_stock=50, min_stock=20, supplier="Пекарня"),
        ]
        
        for item in inventory_items:
            db.add(item)
        
        db.commit()
        print("warehouse added")
        
        # Получаем ID созданных записей для создания рецептов
        menu_items_in_db = db.query(MenuItem).all()
        inventory_items_in_db = db.query(Inventory).all()
        
        # Создаем словари для быстрого поиска по имени
        menu_dict = {item.name: item.id for item in menu_items_in_db}
        inventory_dict = {item.name: item.id for item in inventory_items_in_db}
        
        # Добавляем тестовые рецепты
        recipes = [
            # Стейк Рибай
            Recipe(menu_item_id=menu_dict["Стейк Рибай"], inventory_id=inventory_dict["Говядина"], quantity_required=0.3),
            
            # Цезарь с курицей
            Recipe(menu_item_id=menu_dict["Цезарь с курицей"], inventory_id=inventory_dict["Куриное филе"], quantity_required=0.2),
            Recipe(menu_item_id=menu_dict["Цезарь с курицей"], inventory_id=inventory_dict["Сыр пармезан"], quantity_required=0.05),
            Recipe(menu_item_id=menu_dict["Цезарь с курицей"], inventory_id=inventory_dict["Салат Айсберг"], quantity_required=0.1),
            
            # Кофе латте
            Recipe(menu_item_id=menu_dict["Кофе латте"], inventory_id=inventory_dict["Кофе зерновой"], quantity_required=0.02),
            
            # Бургер
            Recipe(menu_item_id=menu_dict["Бургер"], inventory_id=inventory_dict["Говядина"], quantity_required=0.15),
            Recipe(menu_item_id=menu_dict["Бургер"], inventory_id=inventory_dict["Хлебные булочки"], quantity_required=1),
            
            # Греческий салат
            Recipe(menu_item_id=menu_dict["Греческий салат"], inventory_id=inventory_dict["Помидоры"], quantity_required=0.2),
            Recipe(menu_item_id=menu_dict["Греческий салат"], inventory_id=inventory_dict["Сыр пармезан"], quantity_required=0.08),
        ]
        
        for recipe in recipes:
            db.add(recipe)
        
        db.commit()
        print("recipies added")
        
        # Добавляем тестовые заказы
        orders = [
            Order(customer_name="Иван Петров", phone="+7 (912) 345-67-89", status="Новый", total=2500),
            Order(customer_name="Мария Сидорова", phone="+7 (923) 456-78-90", status="Готовится", total=1800),
            Order(customer_name="Алексей Иванов", phone="+7 (934) 567-89-01", status="Готов к выдаче", total=3200),
        ]
        
        for order in orders:
            db.add(order)
        
        db.commit()
        print("orders added")
        print("TEST DATA ADDED")
        
    except Exception as e:
        print(f"Error while adding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()