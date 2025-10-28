from config.database import engine, Base
from models import Order, MenuItem, Inventory, OrderItem, Recipe

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully")