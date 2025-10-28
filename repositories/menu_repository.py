from sqlalchemy.orm import Session
from models.menu_model import MenuItem
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