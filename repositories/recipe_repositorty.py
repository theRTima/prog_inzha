from sqlalchemy.orm import Session
from models import Recipe
from models import MenuItem
from models import Inventory
from typing import List, Optional

class RecipeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_recipe_for_menu_item(self, menu_item_id: int) -> List[Recipe]:
        return self.db.query(Recipe).filter(Recipe.menu_item_id == menu_item_id).all()

    def add_recipe_item(self, menu_item_id: int, inventory_id: int, quantity_required: float) -> Recipe:
        recipe_item = Recipe(
            menu_item_id=menu_item_id,
            inventory_id=inventory_id,
            quantity_required=quantity_required
        )
        self.db.add(recipe_item)
        self.db.commit()
        self.db.refresh(recipe_item)
        return recipe_item

    def update_recipe_item(self, recipe_id: int, quantity_required: float) -> Optional[Recipe]:
        recipe_item = self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if recipe_item:
            recipe_item.quantity_required = quantity_required
            self.db.commit()
            self.db.refresh(recipe_item)
        return recipe_item

    def delete_recipe_item(self, recipe_id: int) -> bool:
        recipe_item = self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if recipe_item:
            self.db.delete(recipe_item)
            self.db.commit()
            return True
        return False

    def check_ingredient_availability(self, menu_item_id: int) -> bool:
        """Проверяет, достаточно ли ингредиентов для блюда"""
        recipe_items = self.get_recipe_for_menu_item(menu_item_id)
        for recipe in recipe_items:
            if recipe.inventory_item.current_stock < recipe.quantity_required:
                return False
        return True

    def update_menu_item_availability(self, menu_item_id: int):
        """Обновляет доступность блюда на основе остатков ингредиентов"""
        menu_item = self.db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        if menu_item:
            is_available = self.check_ingredient_availability(menu_item_id)
            menu_item.available = is_available
            self.db.commit()