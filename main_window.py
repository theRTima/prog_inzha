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
        self.setWindowTitle('Информационная система ресторана')
        self.setGeometry(100, 100, 1200, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        title_label = QLabel('Система управления заказами навынос')
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        self.order_tab = OrderTab()
        self.menu_tab = MenuTab()
        self.inventory_tab = InventoryTab()
        self.reports_tab = ReportsTab()

        tab_widget.addTab(self.order_tab, 'Заказы')
        tab_widget.addTab(self.menu_tab, 'Меню')
        tab_widget.addTab(self.inventory_tab, 'Склад')
        tab_widget.addTab(self.reports_tab, 'Отчеты')