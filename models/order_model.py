from sqlalchemy import Column, Integer, String, DateTime, Boolean, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    status = Column(String(50), default="Новый")
    created = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    total = Column(DECIMAL(10, 2), default=0)
    
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def formatted_created(self):
        return self.created.strftime("%Y-%m-%d %H:%M") if self.created else ""

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu.id"))
    quantity = Column(Integer, default=1)
    price = Column(DECIMAL(10, 2))
    
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")