from sqlalchemy.orm import Session
from models.models import Inventory
from typing import List, Optional, Dict, Any
from datetime import datetime

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

    def get_inventory_report(self) -> Dict[str, Any]:
        """Отчет по остаткам на складе"""
        try:
            all_items = self.db.query(Inventory).all()
            low_stock_items = self.get_low_stock_items()
            
            # Статистика по категориям
            category_stats = {}
            
            for item in all_items:
                category = item.category
                if category not in category_stats:
                    category_stats[category] = {
                        'count': 0,
                        'items': []
                    }
                
                category_stats[category]['count'] += 1
                category_stats[category]['items'].append({
                    'name': item.name,
                    'current_stock': float(item.current_stock),
                    'unit': item.unit,
                    'min_stock': float(item.min_stock)
                })
            
            # Преобразуем объекты Inventory в словари для избежания проблем с сессией
            low_stock_items_data = []
            for item in low_stock_items:
                low_stock_items_data.append({
                    'id': item.id,
                    'name': item.name,
                    'category': item.category,
                    'unit': item.unit,
                    'current_stock': float(item.current_stock),
                    'min_stock': float(item.min_stock),
                    'supplier': item.supplier
                })
            
            # Преобразуем все items в словари
            all_items_data = []
            for item in all_items:
                all_items_data.append({
                    'id': item.id,
                    'name': item.name,
                    'category': item.category,
                    'unit': item.unit,
                    'current_stock': float(item.current_stock),
                    'min_stock': float(item.min_stock),
                    'supplier': item.supplier
                })
            
            return {
                'total_items': len(all_items),
                'low_stock_count': len(low_stock_items),
                'low_stock_items': low_stock_items_data,
                'category_stats': category_stats,
                'all_items': all_items_data,
                'report_date': datetime.now()
            }
            
        except Exception as e:
            raise e