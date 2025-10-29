from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QDoubleSpinBox, QCheckBox, 
                             QTextEdit, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt

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
        layout.addWidget(QLabel('Цена:'))
        self.price_spinbox = QDoubleSpinBox()
        self.price_spinbox.setMaximum(10000)
        self.price_spinbox.setSuffix(' руб.')
        layout.addWidget(self.price_spinbox)
        
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
        self.price_spinbox.setValue(dish_data.get('price', 0))
        self.available_checkbox.setChecked(dish_data.get('available', True))
        self.description_edit.setPlainText(dish_data.get('description', ''))

    def validate_and_accept(self):
        """Проверяет данные и закрывает диалог с принятием"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, 'Ошибка', 'Введите название блюда')
            return
        
        if self.price_spinbox.value() <= 0:
            QMessageBox.warning(self, 'Ошибка', 'Цена должна быть больше 0')
            return
        
        self.accept()

    def get_dish_data(self):
        """Возвращает данные блюда из формы"""
        return {
            'name': self.name_edit.text().strip(),
            'category': self.category_combo.currentText(),
            'price': self.price_spinbox.value(),
            'available': self.available_checkbox.isChecked(),
            'description': self.description_edit.toPlainText().strip()
        }