from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from widgets.order_tab import OrderTab
from widgets.menu_tab import MenuTab
from widgets.inventory_tab import InventoryTab
from widgets.reports_tab import ReportsTab

class RestaurantOrderSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Информационная система ресторана - Заказы навынос')
        self.setGeometry(100, 100, 1200, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        
        # Создаем вкладки
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # Инициализация вкладок
        self.order_tab = OrderTab()
        self.menu_tab = MenuTab()
        self.inventory_tab = InventoryTab()
        self.reports_tab = ReportsTab()

        tab_widget.addTab(self.order_tab, 'Заказы')
        tab_widget.addTab(self.menu_tab, 'Меню')
        tab_widget.addTab(self.inventory_tab, 'Инвентарь')
        tab_widget.addTab(self.reports_tab, 'Отчеты')

        self.statusBar().showMessage('Готов к работе')