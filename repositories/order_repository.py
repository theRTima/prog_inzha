from sqlalchemy.orm import Session
from models.order_model import Order, OrderItem
from models.menu_model import MenuItem
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
            for key, value in kwargs.items():
                if hasattr(order, key):
                    setattr(order, key, value)
            self.db.commit()
            self.db.refresh(order)
        return order
    
    def delete_order(self, order_id: int) -> bool:
        order = self.get_order(order_id)
        if order:
            self.db.delete(order)
            self.db.commit()
            return True
        return False
    
    def add_order_item(self, order_id: int, menu_item_id: int, quantity: int) -> OrderItem:
        menu_item = self.db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        if not menu_item:
            raise ValueError("Блюдо не найдено")
        
        # Проверяем доступность блюда
        if not menu_item.available:
            raise ValueError("Блюдо недоступно для заказа")
        
        # Создаем позицию заказа
        order_item = OrderItem(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            price=menu_item.price
        )
        self.db.add(order_item)
        self.db.commit()
        self.db.refresh(order_item)
        
        # Обновляем общую сумму заказа
        self._update_order_total(order_id)
        return order_item

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