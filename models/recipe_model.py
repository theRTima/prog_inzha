from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from config.database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu.id"))
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    quantity_required = Column(DECIMAL(10, 3))
    
    menu_item = relationship("MenuItem", back_populates="recipe_items")
    inventory_item = relationship("Inventory")