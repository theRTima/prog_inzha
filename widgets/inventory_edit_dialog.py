from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator

class InventoryEditDialog(QDialog):
    def __init__(self, parent=None, inventory_data=None):
        super().__init__(parent)
        self.inventory_data = inventory_data
        self.initUI()
        
        if inventory_data:
            self.fill_form(inventory_data)

    def initUI(self):
        self.setWindowTitle('Добавить материал' if not self.inventory_data else 'Редактировать материал')
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Название материала
        layout.addWidget(QLabel('Название:'))
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)
        
        # Категория
        layout.addWidget(QLabel('Категория:'))
        self.category_combo = QComboBox()
        self.category_combo.addItems(['Мясо', 'Овощи', 'Молочные', 'Бакалея', 'Напитки', 'Прочее'])
        layout.addWidget(self.category_combo)
        
        # Единица измерения
        layout.addWidget(QLabel('Единица измерения:'))
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(['кг', 'г', 'л', 'мл', 'шт'])
        layout.addWidget(self.unit_combo)
        
        # Текущий остаток
        stock_layout = QHBoxLayout()
        stock_layout.addWidget(QLabel('Текущий остаток:'))
        self.current_stock_edit = QLineEdit()
        
        # Настраиваем валидатор для 3 знаков после запятой
        validator_current = QDoubleValidator(0, 100000, 3, self)
        validator_current.setNotation(QDoubleValidator.StandardNotation)
        self.current_stock_edit.setValidator(validator_current)
        
        self.current_stock_edit.setPlaceholderText("0.000")
        stock_layout.addWidget(self.current_stock_edit)
        stock_layout.addStretch()
        layout.addLayout(stock_layout)
        
        # Минимальный остаток
        min_stock_layout = QHBoxLayout()
        min_stock_layout.addWidget(QLabel('Минимальный остаток:'))
        self.min_stock_edit = QLineEdit()
        
        # Настраиваем валидатор для 3 знаков после запятой
        validator_min = QDoubleValidator(0, 100000, 3, self)
        validator_min.setNotation(QDoubleValidator.StandardNotation)
        self.min_stock_edit.setValidator(validator_min)
        
        self.min_stock_edit.setPlaceholderText("0.000")
        min_stock_layout.addWidget(self.min_stock_edit)
        min_stock_layout.addStretch()
        layout.addLayout(min_stock_layout)
        
        # Поставщик
        layout.addWidget(QLabel('Поставщик:'))
        self.supplier_edit = QLineEdit()
        layout.addWidget(self.supplier_edit)
        
        # Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def fill_form(self, inventory_data):
        self.name_edit.setText(inventory_data.get('name', ''))
        
        category = inventory_data.get('category', 'Мясо')
        index = self.category_combo.findText(category)
        if index >= 0:
            self.category_combo.setCurrentIndex(index)
        
        unit = inventory_data.get('unit', 'кг')
        index = self.unit_combo.findText(unit)
        if index >= 0:
            self.unit_combo.setCurrentIndex(index)
        
        self.current_stock_edit.setText(str(inventory_data.get('current_stock', 0)))
        self.min_stock_edit.setText(str(inventory_data.get('min_stock', 0)))
        self.supplier_edit.setText(inventory_data.get('supplier', ''))

    def validate_and_accept(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, 'Ошибка', 'Введите название материала')
            return
        
        current_stock_text = self.current_stock_edit.text().strip()
        min_stock_text = self.min_stock_edit.text().strip()
        
        # Заменяем запятую на точку для корректного преобразования
        current_stock_text = current_stock_text.replace(',', '.')
        min_stock_text = min_stock_text.replace(',', '.')
        
        try:
            current_stock = float(current_stock_text) if current_stock_text else 0
            min_stock = float(min_stock_text) if min_stock_text else 0
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректные числовые значения для остатков')
            return
        
        if current_stock < 0 or min_stock < 0:
            QMessageBox.warning(self, 'Ошибка', 'Остатки не могут быть отрицательными')
            return
        
        self.accept()

    def get_inventory_data(self):
        current_stock_text = self.current_stock_edit.text().strip()
        min_stock_text = self.min_stock_edit.text().strip()
        
        # Заменяем запятую на точку
        current_stock_text = current_stock_text.replace(',', '.')
        min_stock_text = min_stock_text.replace(',', '.')
        
        current_stock = float(current_stock_text) if current_stock_text else 0
        min_stock = float(min_stock_text) if min_stock_text else 0
        
        return {
            'name': self.name_edit.text().strip(),
            'category': self.category_combo.currentText(),
            'unit': self.unit_combo.currentText(),
            'current_stock': current_stock,
            'min_stock': min_stock,
            'supplier': self.supplier_edit.text().strip()
        }