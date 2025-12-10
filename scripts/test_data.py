import sys
import os
import random
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.models import MenuItem, Inventory, Recipe, Order, OrderItem
from sqlalchemy.sql import text

def seed_database():
    db = SessionLocal()
    
    try:
        # Очищаем таблицы в правильном порядке (с учетом foreign keys)
        db.execute(text("DELETE FROM order_items"))
        db.execute(text("DELETE FROM orders"))
        db.execute(text("DELETE FROM recipes"))
        db.execute(text("DELETE FROM menu_items"))
        db.execute(text("DELETE FROM inventory"))
        
        db.commit()
        print("Старые данные удалены")
        
        # ============== 1. СОЗДАЕМ МЕНЮ (20 позиций) ==============
        menu_items = [
            # Горячие блюда
            MenuItem(name="Стейк Рибай", category="Горячие блюда", price=1200.00, available=True, description="Стейк с картофелем по-деревенски"),
            MenuItem(name="Бургер Классический", category="Горячие блюда", price=550.00, available=True, description="Бургер с говяжьей котлетой"),
            MenuItem(name="Паста Карбонара", category="Горячие блюда", price=650.00, available=True, description="Паста с беконом и сливочным соусом"),
            MenuItem(name="Куриные крылышки", category="Горячие блюда", price=480.00, available=True, description="Крылышки в медово-чесночном соусе"),
            MenuItem(name="Лосось на гриле", category="Горячие блюда", price=950.00, available=True, description="Филе лосося с овощами"),
            
            # Салаты
            MenuItem(name="Цезарь с курицей", category="Салаты", price=450.00, available=True, description="Классический салат Цезарь"),
            MenuItem(name="Греческий салат", category="Салаты", price=420.00, available=True, description="Свежие овощи с сыром фета"),
            MenuItem(name="Оливье", category="Салаты", price=380.00, available=True, description="Салат оливье по-домашнему"),
            MenuItem(name="Салат с креветками", category="Салаты", price=680.00, available=True, description="Салат с тигровыми креветками"),
            
            # Супы
            MenuItem(name="Томатный суп", category="Супы", price=350.00, available=True, description="Томатный суп с базиликом"),
            MenuItem(name="Борщ", category="Супы", price=320.00, available=True, description="Борщ со сметаной"),
            MenuItem(name="Грибной крем-суп", category="Супы", price=380.00, available=True, description="Крем-суп из шампиньонов"),
            
            # Десерты
            MenuItem(name="Тирамису", category="Десерты", price=400.00, available=True, description="Классический итальянский десерт"),
            MenuItem(name="Чизкейк Нью-Йорк", category="Десерты", price=450.00, available=True, description="Чизкейк с ягодным соусом"),
            MenuItem(name="Шоколадный фондан", category="Десерты", price=380.00, available=True, description="Шоколадный кекс с жидкой серединкой"),
            
            # Напитки
            MenuItem(name="Кофе латте", category="Напитки", price=250.00, available=True, description="Кофе латте 300 мл"),
            MenuItem(name="Капучино", category="Напитки", price=230.00, available=True, description="Капучино 250 мл"),
            MenuItem(name="Свежевыжатый апельсиновый сок", category="Напитки", price=320.00, available=True, description="Сок из свежих апельсинов 300 мл"),
            MenuItem(name="Мохито", category="Напитки", price=450.00, available=True, description="Классический мохито 400 мл"),
            MenuItem(name="Чай зеленый", category="Напитки", price=150.00, available=True, description="Зеленый чай с жасмином"),
        ]
        
        for item in menu_items:
            db.add(item)
        
        db.commit()
        print("Меню добавлено (20 позиций)")
        
        # ============== 2. СОЗДАЕМ СКЛАД (25 позиций) ==============
        inventory_items = [
            # Мясо
            Inventory(name="Говядина", category="Мясо", unit="кг", current_stock=25.5, min_stock=10.0, supplier="Мясной двор"),
            Inventory(name="Куриное филе", category="Мясо", unit="кг", current_stock=18.2, min_stock=8.0, supplier="Птицефабрика 'Рассвет'"),
            Inventory(name="Свинина", category="Мясо", unit="кг", current_stock=12.7, min_stock=5.0, supplier="Мясной двор"),
            Inventory(name="Бекон", category="Мясо", unit="кг", current_stock=8.5, min_stock=3.0, supplier="Мясной двор"),
            Inventory(name="Куриные крылышки", category="Мясо", unit="кг", current_stock=15.3, min_stock=6.0, supplier="Птицефабрика 'Рассвет'"),
            
            # Рыба
            Inventory(name="Лосось", category="Рыба", unit="кг", current_stock=9.8, min_stock=4.0, supplier="Рыбный цех"),
            Inventory(name="Креветки тигровые", category="Рыба", unit="кг", current_stock=5.2, min_stock=2.0, supplier="Океан"),
            
            # Овощи
            Inventory(name="Помидоры", category="Овощи", unit="кг", current_stock=22.0, min_stock=10.0, supplier="Овощная база"),
            Inventory(name="Огурцы", category="Овощи", unit="кг", current_stock=18.5, min_stock=8.0, supplier="Овощная база"),
            Inventory(name="Картофель", category="Овощи", unit="кг", current_stock=35.7, min_stock=15.0, supplier="Овощная база"),
            Inventory(name="Лук репчатый", category="Овощи", unit="кг", current_stock=12.3, min_stock=5.0, supplier="Овощная база"),
            Inventory(name="Салат Айсберг", category="Овощи", unit="кг", current_stock=8.2, min_stock=4.0, supplier="Овощная база"),
            Inventory(name="Шампиньоны", category="Овощи", unit="кг", current_stock=6.5, min_stock=3.0, supplier="Грибная ферма"),
            Inventory(name="Свекла", category="Овощи", unit="кг", current_stock=14.2, min_stock=5.0, supplier="Овощная база"),  # ДОБАВЛЕНО
            Inventory(name="Морковь", category="Овощи", unit="кг", current_stock=16.8, min_stock=7.0, supplier="Овощная база"),  # ДОБАВЛЕНО
            Inventory(name="Капуста", category="Овощи", unit="кг", current_stock=12.5, min_stock=6.0, supplier="Овощная база"),  # ДОБАВЛЕНО
            
            # Молочные
            Inventory(name="Сыр пармезан", category="Молочные", unit="кг", current_stock=4.5, min_stock=2.0, supplier="Сыроварня 'Итальянская'"),
            Inventory(name="Сыр фета", category="Молочные", unit="кг", current_stock=3.8, min_stock=2.0, supplier="Греческая сыроварня"),
            Inventory(name="Сливки 33%", category="Молочные", unit="л", current_stock=12.0, min_stock=5.0, supplier="Молочный комбинат"),
            Inventory(name="Сметана", category="Молочные", unit="кг", current_stock=9.5, min_stock=4.0, supplier="Молочный комбинат"),
            
            # Бакалея
            Inventory(name="Кофе зерновой", category="Бакалея", unit="кг", current_stock=8.0, min_stock=3.0, supplier="Кофейная компания"),
            Inventory(name="Паста спагетти", category="Бакалея", unit="кг", current_stock=15.2, min_stock=6.0, supplier="Итальянские продукты"),
            Inventory(name="Хлебные булочки", category="Бакалея", unit="шт", current_stock=120, min_stock=50, supplier="Пекарня 'Сдоба'"),
            
            # Напитки
            Inventory(name="Апельсины", category="Напитки", unit="кг", current_stock=25.0, min_stock=10.0, supplier="Фруктовый рынок"),
            Inventory(name="Чай зеленый", category="Напитки", unit="кг", current_stock=3.5, min_stock=1.5, supplier="Чайная компания"),
            Inventory(name="Лайм", category="Напитки", unit="кг", current_stock=7.3, min_stock=3.0, supplier="Фруктовый рынок"),
            Inventory(name="Мята", category="Напитки", unit="кг", current_stock=2.1, min_stock=1.0, supplier="Травы свежие"),
        ]
        
        for item in inventory_items:
            db.add(item)
        
        db.commit()
        print("Склад заполнен (25 позиций)")
        
        # ============== 3. СОЗДАЕМ РЕЦЕПТЫ ==============
        # Получаем ID созданных записей для создания рецептов
        menu_items_in_db = db.query(MenuItem).all()
        inventory_items_in_db = db.query(Inventory).all()
        
        # Создаем словари для быстрого поиска по имени
        menu_dict = {item.name: item.id for item in menu_items_in_db}
        inventory_dict = {item.name: item.id for item in inventory_items_in_db}
        
        # Добавляем рецепты для каждого блюда
        recipes = [
            # Стейк Рибай
            Recipe(menu_item_id=menu_dict["Стейк Рибай"], inventory_id=inventory_dict["Говядина"], quantity_required=0.3),
            Recipe(menu_item_id=menu_dict["Стейк Рибай"], inventory_id=inventory_dict["Картофель"], quantity_required=0.2),
            
            # Бургер Классический
            Recipe(menu_item_id=menu_dict["Бургер Классический"], inventory_id=inventory_dict["Говядина"], quantity_required=0.15),
            Recipe(menu_item_id=menu_dict["Бургер Классический"], inventory_id=inventory_dict["Хлебные булочки"], quantity_required=1),
            Recipe(menu_item_id=menu_dict["Бургер Классический"], inventory_id=inventory_dict["Помидоры"], quantity_required=0.05),
            Recipe(menu_item_id=menu_dict["Бургер Классический"], inventory_id=inventory_dict["Огурцы"], quantity_required=0.05),
            
            # Паста Карбонара
            Recipe(menu_item_id=menu_dict["Паста Карбонара"], inventory_id=inventory_dict["Паста спагетти"], quantity_required=0.18),
            Recipe(menu_item_id=menu_dict["Паста Карбонара"], inventory_id=inventory_dict["Бекон"], quantity_required=0.1),
            Recipe(menu_item_id=menu_dict["Паста Карбонара"], inventory_id=inventory_dict["Сливки 33%"], quantity_required=0.08),
            
            # Куриные крылышки
            Recipe(menu_item_id=menu_dict["Куриные крылышки"], inventory_id=inventory_dict["Куриные крылышки"], quantity_required=0.25),
            
            # Лосось на гриле
            Recipe(menu_item_id=menu_dict["Лосось на гриле"], inventory_id=inventory_dict["Лосось"], quantity_required=0.2),
            Recipe(menu_item_id=menu_dict["Лосось на гриле"], inventory_id=inventory_dict["Огурцы"], quantity_required=0.1),
            Recipe(menu_item_id=menu_dict["Лосось на гриле"], inventory_id=inventory_dict["Помидоры"], quantity_required=0.1),
            
            # Цезарь с курицей
            Recipe(menu_item_id=menu_dict["Цезарь с курицей"], inventory_id=inventory_dict["Куриное филе"], quantity_required=0.15),
            Recipe(menu_item_id=menu_dict["Цезарь с курицей"], inventory_id=inventory_dict["Салат Айсберг"], quantity_required=0.1),
            Recipe(menu_item_id=menu_dict["Цезарь с курицей"], inventory_id=inventory_dict["Сыр пармезан"], quantity_required=0.05),
            
            # Греческий салат
            Recipe(menu_item_id=menu_dict["Греческий салат"], inventory_id=inventory_dict["Помидоры"], quantity_required=0.15),
            Recipe(menu_item_id=menu_dict["Греческий салат"], inventory_id=inventory_dict["Огурцы"], quantity_required=0.1),
            Recipe(menu_item_id=menu_dict["Греческий салат"], inventory_id=inventory_dict["Сыр фета"], quantity_required=0.08),
            
            # Оливье
            Recipe(menu_item_id=menu_dict["Оливье"], inventory_id=inventory_dict["Картофель"], quantity_required=0.1),
            Recipe(menu_item_id=menu_dict["Оливье"], inventory_id=inventory_dict["Огурцы"], quantity_required=0.05),
            Recipe(menu_item_id=menu_dict["Оливье"], inventory_id=inventory_dict["Морковь"], quantity_required=0.05),  # ДОБАВЛЕНО
            
            # Салат с креветками
            Recipe(menu_item_id=menu_dict["Салат с креветками"], inventory_id=inventory_dict["Креветки тигровые"], quantity_required=0.12),
            Recipe(menu_item_id=menu_dict["Салат с креветками"], inventory_id=inventory_dict["Салат Айсберг"], quantity_required=0.08),
            
            # Томатный суп
            Recipe(menu_item_id=menu_dict["Томатный суп"], inventory_id=inventory_dict["Помидоры"], quantity_required=0.25),
            Recipe(menu_item_id=menu_dict["Томатный суп"], inventory_id=inventory_dict["Сливки 33%"], quantity_required=0.05),
            
            # Борщ
            Recipe(menu_item_id=menu_dict["Борщ"], inventory_id=inventory_dict["Картофель"], quantity_required=0.15),
            Recipe(menu_item_id=menu_dict["Борщ"], inventory_id=inventory_dict["Свекла"], quantity_required=0.1),
            Recipe(menu_item_id=menu_dict["Борщ"], inventory_id=inventory_dict["Капуста"], quantity_required=0.08),  # ДОБАВЛЕНО
            Recipe(menu_item_id=menu_dict["Борщ"], inventory_id=inventory_dict["Морковь"], quantity_required=0.05),  # ДОБАВЛЕНО
            Recipe(menu_item_id=menu_dict["Борщ"], inventory_id=inventory_dict["Сметана"], quantity_required=0.03),
            
            # Грибной крем-суп
            Recipe(menu_item_id=menu_dict["Грибной крем-суп"], inventory_id=inventory_dict["Шампиньоны"], quantity_required=0.2),
            Recipe(menu_item_id=menu_dict["Грибной крем-суп"], inventory_id=inventory_dict["Сливки 33%"], quantity_required=0.1),
            
            # Тирамису
            Recipe(menu_item_id=menu_dict["Тирамису"], inventory_id=inventory_dict["Сливки 33%"], quantity_required=0.15),
            
            # Чизкейк Нью-Йорк
            Recipe(menu_item_id=menu_dict["Чизкейк Нью-Йорк"], inventory_id=inventory_dict["Сливки 33%"], quantity_required=0.2),
            
            # Шоколадный фондан
            Recipe(menu_item_id=menu_dict["Шоколадный фондан"], inventory_id=inventory_dict["Сливки 33%"], quantity_required=0.12),
            
            # Кофе латте
            Recipe(menu_item_id=menu_dict["Кофе латте"], inventory_id=inventory_dict["Кофе зерновой"], quantity_required=0.02),
            Recipe(menu_item_id=menu_dict["Кофе латте"], inventory_id=inventory_dict["Сливки 33%"], quantity_required=0.05),
            
            # Капучино
            Recipe(menu_item_id=menu_dict["Капучино"], inventory_id=inventory_dict["Кофе зерновой"], quantity_required=0.02),
            Recipe(menu_item_id=menu_dict["Капучино"], inventory_id=inventory_dict["Сливки 33%"], quantity_required=0.04),
            
            # Свежевыжатый апельсиновый сок
            Recipe(menu_item_id=menu_dict["Свежевыжатый апельсиновый сок"], inventory_id=inventory_dict["Апельсины"], quantity_required=0.3),
            
            # Мохито
            Recipe(menu_item_id=menu_dict["Мохито"], inventory_id=inventory_dict["Лайм"], quantity_required=0.05),
            Recipe(menu_item_id=menu_dict["Мохито"], inventory_id=inventory_dict["Мята"], quantity_required=0.01),
            
            # Чай зеленый
            Recipe(menu_item_id=menu_dict["Чай зеленый"], inventory_id=inventory_dict["Чай зеленый"], quantity_required=0.005),
        ]
        
        for recipe in recipes:
            db.add(recipe)
        
        db.commit()
        print("Рецепты добавлены (47 рецептов)")
        
        # ============== 4. СОЗДАЕМ ЗАКАЗЫ (15 заказов) ==============
        # Создаем заказы с разными датами (последние 30 дней)
        orders = []
        statuses = ['Новый', 'Подтвержден', 'Готовится', 'Готов к выдаче', 'Выдан', 'Отменен']
        
        for i in range(1, 16):
            # Генерируем случайную дату в пределах последних 30 дней
            days_ago = random.randint(0, 30)
            order_date = datetime.now() - timedelta(days=days_ago)
            
            order = Order(
                customer_name=f"Клиент {i}",
                phone=f"+7 (9{random.randint(10, 99)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
                status=random.choice(statuses),
                created=order_date,
                notes=f"Тестовый заказ №{i}" if i % 3 == 0 else None,
                total=0  # Временно 0, посчитаем после добавления позиций
            )
            db.add(order)
            db.flush()  # Получаем ID заказа без коммита
            orders.append(order)
        
        db.commit()
        print("Заказы созданы (15 заказов)")
        
        # ============== 5. ДОБАВЛЯЕМ ПОЗИЦИИ В ЗАКАЗЫ ==============
        # Список популярных блюд для добавления в заказы
        popular_dishes = [
            ("Стейк Рибай", 1200.00),
            ("Бургер Классический", 550.00),
            ("Цезарь с курицей", 450.00),
            ("Паста Карбонара", 650.00),
            ("Томатный суп", 350.00),
            ("Кофе латте", 250.00),
            ("Тирамису", 400.00),
            ("Греческий салат", 420.00),
            ("Куриные крылышки", 480.00),
            ("Капучино", 230.00),
        ]
        
        # Для каждого заказа добавляем 1-4 позиции
        order_totals = {}
        
        for order in orders:
            total = 0
            num_items = random.randint(1, 4)
            
            for _ in range(num_items):
                dish_name, price = random.choice(popular_dishes)
                quantity = random.randint(1, 3)
                
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_dict[dish_name],
                    quantity=quantity,
                    price=price
                )
                db.add(order_item)
                total += price * quantity
            
            order_totals[order.id] = total
        
        db.commit()
        print("Позиции заказов добавлены")
        
        # ============== 6. ОБНОВЛЯЕМ СУММЫ ЗАКАЗОВ ==============
        for order in orders:
            order.total = order_totals[order.id]
        
        db.commit()
        print("Суммы заказов обновлены")
        
        # ============== 7. ОБНОВЛЯЕМ ДОСТУПНОСТЬ БЛЮД ==============
        # Импортируем RecipeRepository для обновления доступности
        from repositories.recipe_repository import RecipeRepository
        recipe_repo = RecipeRepository(db)
        
        # Обновляем доступность всех блюд
        for menu_item in menu_items_in_db:
            recipe_repo.update_menu_item_availability(menu_item.id)
        
        db.commit()
        
        print("=" * 50)
        print("ТЕСТОВЫЕ ДАННЫЕ УСПЕШНО ДОБАВЛЕНЫ:")
        print(f"- Меню: {len(menu_items)} позиций")
        print(f"- Склад: {len(inventory_items)} позиций")
        print(f"- Рецепты: {len(recipes)} позиций")
        print(f"- Заказы: {len(orders)} позиций")
        print("=" * 50)
        
    except Exception as e:
        print(f"Ошибка при добавлении данных: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()