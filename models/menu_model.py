from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, Text
from sqlalchemy.orm import relationship
from config.database import Base

class MenuItem(Base):
    __tablename__ = "menu"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    price = Column(DECIMAL(10, 2))
    available = Column(Boolean, default=True)
    description = Column(Text)
    
    recipe_items = relationship("Recipe", back_populates="menu_item")