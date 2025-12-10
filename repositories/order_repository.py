from sqlalchemy.orm import Session
from models.models import Order, OrderItem, MenuItem, Inventory
from typing import List, Optional

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_order(self, customer_name: str, phone: str, notes: str = "") -> Order:
        order = Order(
            customer_name=customer_name,
            phone=phone,
            notes=notes,
            status="Новый"
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_order(self, order_id: int) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def get_all_orders(self) -> List[Order]:
        return self.db.query(Order).order_by(Order.created.desc()).all()
    
    def update_order(self, order_id: int, **kwargs) -> Optional[Order]:
        order = self.get_order(order_id)
        if order:
            old_status = order.status
            new_status = kwargs.get('status')
            
            # Обновляем поля заказа
            for key, value in kwargs.items():
                if hasattr(order, key):
                    setattr(order, key, value)
            
            # Сначала списываем ингредиенты, если статус меняется на "Подтвержден"
            if new_status == "Подтвержден" and old_status != "Подтвержден":
                try:
                    self.deduct_inventory_for_order(order_id)
                except Exception as e:
                    # Если списание не удалось, откатываем изменения
                    self.db.rollback()
                    raise e
            
            # Сохраняем изменения в заказе
            self.db.commit()
            self.db.refresh(order)
                
        return order
    
    def delete_order(self, order_id: int) -> bool:
        order = self.get_order(order_id)
        if order:
            # Если заказ был подтвержден, возвращаем ингредиенты
            if order.status == "Подтвержден":
                try:
                    self.return_inventory_for_order(order_id)
                except Exception:
                    pass  # Игнорируем ошибки при возврате
            
            self.db.delete(order)
            self.db.commit()
            return True
        return False
    
    def add_order_item(self, order_id: int, menu_item_id: int, quantity: int):
        menu_item = self.db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        if not menu_item:
            raise ValueError("Блюдо не найдено")
        
        # Проверяем доступность блюда
        if not menu_item.available:
            raise ValueError("Блюдо недоступно для заказа")
        
        order_item = OrderItem(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            price=menu_item.price
        )
        self.db.add(order_item)
        self.db.commit()
        
        # Обновляем общую сумму заказа
        self._update_order_total(order_id)
    
    def remove_order_item(self, order_item_id: int):
        order_item = self.db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
        if order_item:
            order_id = order_item.order_id
            self.db.delete(order_item)
            self.db.commit()
            self._update_order_total(order_id)
    
    def _update_order_total(self, order_id: int):
        order = self.get_order(order_id)
        if order:
            total = sum(item.quantity * item.price for item in order.items)
            order.total = total
            self.db.commit()
    
    def deduct_inventory_for_order(self, order_id: int):
        """Списывает ингредиенты для подтвержденного заказа"""
        order = self.get_order(order_id)
        if not order:
            raise ValueError(f"Заказ #{order_id} не найден")
        
        if not order.items:
            raise ValueError(f"В заказе #{order_id} нет позиций")
        
        errors = []
        warnings = []
        
        try:
            for order_item in order.items:
                menu_item = order_item.menu_item
                quantity = order_item.quantity
                
                # Получаем рецепт блюда
                from repositories.recipe_repository import RecipeRepository
                recipe_repo = RecipeRepository(self.db)
                recipe_items = recipe_repo.get_recipe_for_menu_item(menu_item.id)
                
                if not recipe_items:
                    errors.append(f"У блюда '{menu_item.name}' нет рецепта")
                    continue
                
                dish_errors = []
                for recipe_item in recipe_items:
                    inventory_item = recipe_item.inventory_item
                    required_quantity = recipe_item.quantity_required * quantity
                    
                    # Проверяем достаточно ли ингредиентов
                    if inventory_item.current_stock < required_quantity:
                        dish_errors.append(
                            f"  - {inventory_item.name}: требуется {required_quantity:.3f} {inventory_item.unit}, "
                            f"доступно {inventory_item.current_stock:.3f} {inventory_item.unit}"
                        )
                
                if dish_errors:
                    errors.append(f"Блюдо: {menu_item.name} (количество: {quantity}):")
                    errors.extend(dish_errors)
                else:
                    # Если ингредиентов достаточно, списываем их
                    for recipe_item in recipe_items:
                        inventory_item = recipe_item.inventory_item
                        required_quantity = recipe_item.quantity_required * quantity
                        inventory_item.current_stock -= required_quantity
                    
                    # Обновляем доступность блюда после списания
                    recipe_repo.update_menu_item_availability(menu_item.id)
            
            if errors:
                error_message = "\n".join(errors)
                self.db.rollback()  # Откатываем изменения
                
                # Формируем понятное сообщение для пользователя
                full_message = (
                    f"Невозможно подтвердить заказ #{order_id}.\n\n"
                    f"Причина: недостаточно ингредиентов для приготовления:\n\n"
                    f"{error_message}\n\n"
                    f"Пожалуйста, пополните склад или удалите недоступные блюда из заказа."
                )
                raise ValueError(full_message)
            
            # Сохраняем изменения
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            raise e
    
    def return_inventory_for_order(self, order_id: int):
        """Возвращает ингредиенты при отмене подтвержденного заказа"""
        order = self.get_order(order_id)
        if not order:
            return
        
        try:
            for order_item in order.items:
                menu_item = order_item.menu_item
                quantity = order_item.quantity
                
                # Получаем рецепт блюда
                from repositories.recipe_repository import RecipeRepository
                recipe_repo = RecipeRepository(self.db)
                recipe_items = recipe_repo.get_recipe_for_menu_item(menu_item.id)
                
                for recipe_item in recipe_items:
                    inventory_item = recipe_item.inventory_item
                    required_quantity = recipe_item.quantity_required * quantity
                    
                    # Возвращаем ингредиенты
                    inventory_item.current_stock += required_quantity
                
                # Обновляем доступность блюда после возврата
                recipe_repo.update_menu_item_availability(menu_item.id)
            
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            raise e