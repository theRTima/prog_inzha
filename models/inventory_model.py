from sqlalchemy import Column, Integer, String, DECIMAL
from config.database import Base

class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    unit = Column(String(20))
    current_stock = Column(DECIMAL(10, 3))
    min_stock = Column(DECIMAL(10, 3))
    supplier = Column(String(100))