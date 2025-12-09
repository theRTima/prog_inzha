from sqlalchemy.orm import Session
from models.models import MenuItem  # Обновленный импорт
from typing import List, Optional

class MenuRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_menu_items(self) -> List[MenuItem]:
        return self.db.query(MenuItem).filter(MenuItem.available == True).all()
    
    def get_menu_item(self, item_id: int) -> Optional[MenuItem]:
        return self.db.query(MenuItem).filter(MenuItem.id == item_id).first()
    
    def get_menu_items_by_category(self, category: str) -> List[MenuItem]:
        return self.db.query(MenuItem).filter(
            MenuItem.category == category, 
            MenuItem.available == True
        ).all()
    
    def create_menu_item(self, name: str, category: str, price: float, 
                        available: bool = True, description: str = "") -> MenuItem:
        menu_item = MenuItem(
            name=name,
            category=category,
            price=price,
            available=available,
            description=description
        )
        self.db.add(menu_item)
        self.db.commit()
        self.db.refresh(menu_item)
        return menu_item
    
    def update_menu_item(self, item_id: int, **kwargs) -> Optional[MenuItem]:
        menu_item = self.get_menu_item(item_id)
        if menu_item:
            for key, value in kwargs.items():
                if hasattr(menu_item, key):
                    setattr(menu_item, key, value)
            self.db.commit()
            self.db.refresh(menu_item)
        return menu_item
    
    def delete_menu_item(self, item_id: int) -> bool:
        menu_item = self.get_menu_item(item_id)
        if menu_item:
            self.db.delete(menu_item)
            self.db.commit()
            return True
        return False
