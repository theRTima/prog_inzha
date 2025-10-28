import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_db, engine
from models.order_model import Order

def test_db():
    try:
        # Тест подключения
        with engine.connect() as conn:
            print("it works")
        
        # Тест создания таблиц
        with get_db() as db:
            orders = db.query(Order).all()
            print(f"it works. total orders: {len(orders)}")
            
        print("all good!")
        
    except Exception as e:
        print(f"error: {e}")

if __name__ == "__main__":
    test_db()