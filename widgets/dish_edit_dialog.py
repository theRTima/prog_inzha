from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QTextEdit, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QValidator

class DishEditDialog(QDialog):
    def __init__(self, parent=None, dish_data=None):
        super().__init__(parent)
        self.dish_data = dish_data
        self.initUI()
        
        # Если переданы данные блюда, заполняем форму для редактирования
        if dish_data:
            self.fill_form(dish_data)

    def initUI(self):
        self.setWindowTitle('Добавить блюдо' if not self.dish_data else 'Редактировать блюдо')
        self.setModal(True)
        self.resize(400, 500)
        
        layout = QVBoxLayout(self)
        
        # Название блюда
        layout.addWidget(QLabel('Название:'))
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)
        
        # Категория
        layout.addWidget(QLabel('Категория:'))
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            'Горячие блюда', 'Салаты', 'Супы', 'Десерты', 'Напитки'
        ])
        layout.addWidget(self.category_combo)
        
        # Цена
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel('Цена:'))
        self.price_edit = QLineEdit()
        # Устанавливаем валидатор для ввода только чисел
        validator = QDoubleValidator(0, 10000, 2, self)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.price_edit.setValidator(validator)
        self.price_edit.setPlaceholderText("0.00")
        price_layout.addWidget(self.price_edit)
        price_layout.addWidget(QLabel('руб.'))
        price_layout.addStretch()
        layout.addLayout(price_layout)
        
        # Доступность
        self.available_checkbox = QCheckBox('Доступно для заказа')
        self.available_checkbox.setChecked(True)
        layout.addWidget(self.available_checkbox)
        
        # Описание
        layout.addWidget(QLabel('Описание:'))
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        layout.addWidget(self.description_edit)
        
        # Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def fill_form(self, dish_data):
        """Заполняет форму данными блюда для редактирования"""
        self.name_edit.setText(dish_data.get('name', ''))
        category = dish_data.get('category', 'Горячие блюда')
        index = self.category_combo.findText(category)
        if index >= 0:
            self.category_combo.setCurrentIndex(index)
        
        # Устанавливаем цену без форматирования
        price = dish_data.get('price', 0)
        self.price_edit.setText(str(price))
        
        self.available_checkbox.setChecked(dish_data.get('available', True))
        self.description_edit.setPlainText(dish_data.get('description', ''))

    def validate_and_accept(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, 'Ошибка', 'Введите название блюда')
            return
        
        # Проверяем цену
        price_text = self.price_edit.text().strip()
        if not price_text:
            QMessageBox.warning(self, 'Ошибка', 'Введите цену блюда')
            return
        
        # Заменяем запятую на точку
        price_text = price_text.replace(',', '.')
        
        try:
            price = float(price_text)
            if price <= 0:
                QMessageBox.warning(self, 'Ошибка', 'Цена должна быть больше 0')
                return
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректную цену (например: 250.50)')
            return
        
        self.accept()

    def get_dish_data(self):
        """Возвращает данные блюда из формы"""
        price_text = self.price_edit.text().strip()
        # Заменяем запятую на точку
        price_text = price_text.replace(',', '.')
        price = float(price_text) if price_text else 0
        
        return {
            'name': self.name_edit.text().strip(),
            'category': self.category_combo.currentText(),
            'price': price,
            'available': self.available_checkbox.isChecked(),
            'description': self.description_edit.toPlainText().strip()
        }