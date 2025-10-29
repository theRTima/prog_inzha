from sqlalchemy.orm import Session
from models.inventory_model import Inventory
from typing import List, Optional

class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_inventory(self) -> List[Inventory]:
        return self.db.query(Inventory).all()

    def get_inventory_item(self, item_id: int) -> Optional[Inventory]:
        return self.db.query(Inventory).filter(Inventory.id == item_id).first()

    def create_inventory_item(self, name: str, category: str, unit: str, 
                              current_stock: float, min_stock: float, supplier: str) -> Inventory:
        inventory_item = Inventory(
            name=name,
            category=category,
            unit=unit,
            current_stock=current_stock,
            min_stock=min_stock,
            supplier=supplier
        )
        self.db.add(inventory_item)
        self.db.commit()
        self.db.refresh(inventory_item)
        return inventory_item

    def update_inventory_item(self, item_id: int, **kwargs) -> Optional[Inventory]:
        inventory_item = self.get_inventory_item(item_id)
        if inventory_item:
            for key, value in kwargs.items():
                if hasattr(inventory_item, key):
                    setattr(inventory_item, key, value)
            self.db.commit()
            self.db.refresh(inventory_item)
        return inventory_item

    def delete_inventory_item(self, item_id: int) -> bool:
        inventory_item = self.get_inventory_item(item_id)
        if inventory_item:
            self.db.delete(inventory_item)
            self.db.commit()
            return True
        return False

    def get_low_stock_items(self) -> List[Inventory]:
        return self.db.query(Inventory).filter(Inventory.current_stock <= Inventory.min_stock).all()