from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QComboBox, 
                             QSpinBox, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt
from config.database import get_db
from repositories.menu_repository import MenuRepository

class DishSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_dish = None
        self.quantity = 1
        self.initUI()
        self.load_menu_items()
    
    def initUI(self):
        self.setWindowTitle("Добавить блюдо в заказ")
        self.setModal(True)
        self.resize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Фильтр по категориям
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Фильтр по категории:"))
        self.category_filter = QComboBox()
        self.category_filter.addItems([
            "Все категории", "Горячие блюда", "Салаты", "Супы", "Десерты", "Напитки"
        ])
        self.category_filter.currentTextChanged.connect(self.load_menu_items)
        filter_layout.addWidget(self.category_filter)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Таблица меню
        self.menu_table = QTableWidget()
        self.menu_table.setColumnCount(4)
        self.menu_table.setHorizontalHeaderLabels([
            'ID', 'Название', 'Категория', 'Цена'
        ])
        self.menu_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.menu_table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.menu_table)
        
        # Выбор количества
        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(QLabel("Количество:"))
        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setMinimum(1)
        self.quantity_spinbox.setMaximum(100)
        self.quantity_spinbox.setValue(1)
        quantity_layout.addWidget(self.quantity_spinbox)
        quantity_layout.addStretch()
        layout.addLayout(quantity_layout)
        
        # Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept_selection)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_menu_items(self):
        try:
            with get_db() as db:
                repo = MenuRepository(db)
                category = self.category_filter.currentText()
                
                if category == "Все категории":
                    menu_items = repo.get_all_menu_items()
                else:
                    menu_items = repo.get_menu_items_by_category(category)
                
                self.menu_table.setRowCount(len(menu_items))
                for row, item in enumerate(menu_items):
                    self.menu_table.setItem(row, 0, QTableWidgetItem(str(item.id)))
                    self.menu_table.setItem(row, 1, QTableWidgetItem(item.name))
                    self.menu_table.setItem(row, 2, QTableWidgetItem(item.category))
                    self.menu_table.setItem(row, 3, QTableWidgetItem(str(item.price)))
        
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось загрузить меню: {str(e)}')
    
    def accept_selection(self):
        current_row = self.menu_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите блюдо из списка')
            return
        
        dish_id = int(self.menu_table.item(current_row, 0).text())
        dish_name = self.menu_table.item(current_row, 1).text()
        price = float(self.menu_table.item(current_row, 3).text())
        quantity = self.quantity_spinbox.value()
        
        self.selected_dish = {
            'id': dish_id,
            'name': dish_name,
            'price': price,
            'quantity': quantity
        }
        
        self.accept()
    
    def get_selected_dish(self):
        return self.selected_dish