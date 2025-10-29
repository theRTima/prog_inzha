from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, Text
from sqlalchemy.orm import relationship
from config.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"  # Изменяем название таблицы
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    price = Column(DECIMAL(10, 2))
    available = Column(Boolean, default=True)
    description = Column(Text)
    
    # Используем ленивую загрузку для разрыва циклических импортов
    recipe_items = relationship("Recipe", back_populates="menu_item", cascade="all, delete-orphan", lazy="select")