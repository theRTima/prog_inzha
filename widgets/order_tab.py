from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
from config.database import get_db
from repositories.order_repository import OrderRepository

class OrderTab(QWidget):
    order_created = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def populate_orders(self):
        with get_db() as db:
            repo = OrderRepository(db)
            orders = repo.get_all_orders()
            
            self.orders_table.setRowCount(len(orders))
            for row, order in enumerate(orders):
                self.orders_table.setItem(row, 0, QTableWidgetItem(str(order.id)))
                self.orders_table.setItem(row, 1, QTableWidgetItem(order.customer_name))
                self.orders_table.setItem(row, 2, QTableWidgetItem(order.phone or ""))
                self.orders_table.setItem(row, 3, QTableWidgetItem(str(order.total)))
                self.orders_table.setItem(row, 4, QTableWidgetItem(order.status))
                self.orders_table.setItem(row, 5, QTableWidgetItem(order.created.strftime("%Y-%m-%d %H:%M")))
    
    def create_order(self):
        with get_db() as db:
            repo = OrderRepository(db)
            order = repo.create_order(
                customer_name=self.order_customer.text(),
                phone=self.order_phone.text(),
                notes=self.order_notes.toPlainText()
            )
            self.order_created.emit(order)
            self.statusBar().showMessage(f'Создан заказ #{order.id}')