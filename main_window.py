from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                             QMessageBox, QStatusBar)
from PyQt5.QtCore import Qt
from widgets.order_tab import OrderTab
from widgets.menu_tab import MenuTab
from widgets.inventory_tab import InventoryTab
from widgets.reports_tab import ReportsTab

class MainWindow(QMainWindow):
    def __init__(self, role='Владелец'):
        super().__init__()
        self.user_role = role
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(f'Система управления рестораном - {self.user_role}')
        self.setGeometry(100, 100, 1200, 700)
        
        # Создаем центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Создаем вкладки
        self.tab_widget = QTabWidget()
        
        # Создаем колбэк для обновления других вкладок
        def refresh_other_tabs():
            if hasattr(self, 'inventory_tab'):
                self.inventory_tab.refresh_inventory()
            if hasattr(self, 'menu_tab'):
                self.menu_tab.refresh_menu()
        
        # Создаем экземпляры вкладок с передачей колбэка
        self.orders_tab = OrderTab(refresh_callback=refresh_other_tabs)
        self.menu_tab = MenuTab()
        self.inventory_tab = InventoryTab()
        self.reports_tab = ReportsTab()
        
        # Добавляем вкладки в зависимости от роли
        if self.user_role == 'Владелец':
            self.tab_widget.addTab(self.orders_tab, "Заказы")
            self.tab_widget.addTab(self.menu_tab, "Меню")
            self.tab_widget.addTab(self.inventory_tab, "Склад")
            self.tab_widget.addTab(self.reports_tab, "Отчеты")
        
        elif self.user_role == 'Официант':
            self.tab_widget.addTab(self.orders_tab, "Заказы")
            self.tab_widget.addTab(self.menu_tab, "Меню")
            
        elif self.user_role == 'Складовщик':
            self.tab_widget.addTab(self.inventory_tab, "Склад")
            self.tab_widget.addTab(self.menu_tab, "Меню")
            
        elif self.user_role == 'Бухгалтерия':
            self.tab_widget.addTab(self.reports_tab, "Отчеты")
        
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неизвестная роль пользователя')
            return
        
        main_layout.addWidget(self.tab_widget)
        
        # Создаем статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f'Вы вошли как: {self.user_role}')
        
        # Устанавливаем минимальные размеры
        self.setMinimumSize(800, 600)
        
    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        reply = QMessageBox.question(self, 'Подтверждение', 
                                     'Вы уверены, что хотите выйти?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()