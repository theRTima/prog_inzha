from sqlalchemy import Column, Integer, String, DateTime, Boolean, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    price = Column(DECIMAL(10, 2))
    available = Column(Boolean, default=True)
    description = Column(Text)
    
    recipe_items = relationship("Recipe", back_populates="menu_item", cascade="all, delete-orphan", lazy="select")

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    unit = Column(String(20))
    current_stock = Column(DECIMAL(10, 3))
    min_stock = Column(DECIMAL(10, 3))
    supplier = Column(String(100))

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    quantity_required = Column(DECIMAL(10, 3))

    menu_item = relationship("MenuItem", back_populates="recipe_items", lazy="select")
    inventory_item = relationship("Inventory", lazy="select")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    status = Column(String(50), default="Новый")
    created = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    total = Column(DECIMAL(10, 2), default=0)
    
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="select")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, default=1)
    price = Column(DECIMAL(10, 2))
    
    order = relationship("Order", back_populates="items", lazy="select")
    menu_item = relationship("MenuItem", lazy="select")

@property
def formatted_created(self):
    return self.created.strftime("%d.%m.%Y%H:%M") if self.created else None