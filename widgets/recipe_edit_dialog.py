from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QComboBox, 
                             QLineEdit, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from config.database import get_db
from repositories.inventory_repository import InventoryRepository
from repositories.recipe_repository import RecipeRepository

class RecipeEditDialog(QDialog):
    def __init__(self, parent=None, menu_item_id=None, menu_item_name=None):
        super().__init__(parent)
        self.menu_item_id = menu_item_id
        self.menu_item_name = menu_item_name
        self.initUI()
        self.load_recipe()
        self.load_inventory()

    def initUI(self):
        self.setWindowTitle(f'Редактирование рецепта: {self.menu_item_name}')
        self.setModal(True)
        self.resize(600, 500)  # Увеличиваем высоту окна
        
        layout = QVBoxLayout(self)
        
        # Таблица текущего рецепта
        layout.addWidget(QLabel('Текущие ингредиенты:'))
        self.recipe_table = QTableWidget()
        self.recipe_table.setColumnCount(5)
        self.recipe_table.setHorizontalHeaderLabels([
            'ID', 'Ингредиент', 'Количество', 'Ед. изм.', 'Доступно'
        ])
        self.recipe_table.setSortingEnabled(True)
        layout.addWidget(self.recipe_table)
        
        # Панель добавления нового ингредиента
        add_group = QGroupBox('Добавить новый ингредиент')
        add_layout = QVBoxLayout(add_group)
        
        ingredient_layout = QHBoxLayout()
        ingredient_layout.addWidget(QLabel('Ингредиент:'))
        
        self.inventory_combo = QComboBox()
        ingredient_layout.addWidget(self.inventory_combo)
        ingredient_layout.addStretch()
        add_layout.addLayout(ingredient_layout)
        
        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(QLabel('Количество:'))
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setPlaceholderText("0.000")
        
        # Настраиваем валидатор для чисел с 3 знаками после запятой
        validator = QDoubleValidator(0, 1000, 3, self)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.quantity_edit.setValidator(validator)
        
        quantity_layout.addWidget(self.quantity_edit)
        quantity_layout.addStretch()
        add_layout.addLayout(quantity_layout)
        
        btn_add = QPushButton('Добавить в рецепт')
        btn_add.clicked.connect(self.add_ingredient)
        add_layout.addWidget(btn_add)
        
        layout.addWidget(add_group)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        btn_remove = QPushButton('Удалить выбранный ингредиент')
        btn_remove.clicked.connect(self.remove_ingredient)
        button_layout.addWidget(btn_remove)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Информация о блюде
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel(f'Блюдо: {self.menu_item_name}'))
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # Кнопки закрытия
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def load_inventory(self):
        try:
            with get_db() as db:
                repo = InventoryRepository(db)
                inventory_items = repo.get_all_inventory()
                self.inventory_combo.clear()
                for item in inventory_items:
                    self.inventory_combo.addItem(f"{item.name} ({item.unit})", item.id)
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось загрузить инвентарь: {str(e)}')

    def load_recipe(self):
        try:
            with get_db() as db:
                repo = RecipeRepository(db)
                recipe_items = repo.get_recipe_for_menu_item(self.menu_item_id)
                
                self.recipe_table.setRowCount(len(recipe_items))
                for row, item in enumerate(recipe_items):
                    available = item.inventory_item.current_stock >= item.quantity_required
                    available_text = "Да" if available else "Нет"
                    
                    self.recipe_table.setItem(row, 0, QTableWidgetItem(str(item.id)))
                    self.recipe_table.setItem(row, 1, QTableWidgetItem(item.inventory_item.name))
                    self.recipe_table.setItem(row, 2, QTableWidgetItem(str(item.quantity_required)))
                    self.recipe_table.setItem(row, 3, QTableWidgetItem(item.inventory_item.unit))
                    self.recipe_table.setItem(row, 4, QTableWidgetItem(available_text))
                    
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось загрузить рецепт: {str(e)}')

    def add_ingredient(self):
        inventory_id = self.inventory_combo.currentData()
        if not inventory_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите ингредиент')
            return
        
        quantity_text = self.quantity_edit.text().strip()
        if not quantity_text:
            QMessageBox.warning(self, 'Ошибка', 'Введите количество')
            return
        
        # Заменяем запятую на точку для корректного преобразования
        quantity_text = quantity_text.replace(',', '.')
        
        try:
            quantity = float(quantity_text)
            if quantity <= 0:
                QMessageBox.warning(self, 'Ошибка', 'Количество должно быть больше 0')
                return
            
            # Проверяем, что количество не слишком большое
            if quantity > 1000:
                QMessageBox.warning(self, 'Ошибка', 'Количество не может превышать 1000')
                return
                
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректное количество (например: 0.05)')
            return
        
        try:
            with get_db() as db:
                repo = RecipeRepository(db)
                
                # Проверяем, не добавлен ли уже этот ингредиент
                existing_items = repo.get_recipe_for_menu_item(self.menu_item_id)
                for item in existing_items:
                    if item.inventory_id == inventory_id:
                        QMessageBox.warning(self, 'Ошибка', 'Этот ингредиент уже добавлен в рецепт')
                        return
                
                repo.add_recipe_item(self.menu_item_id, inventory_id, quantity)
                # Обновляем доступность блюда
                repo.update_menu_item_availability(self.menu_item_id)
            
            self.load_recipe()
            self.quantity_edit.clear()
            QMessageBox.information(self, 'Успех', 'Ингредиент добавлен в рецепт')
            
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить ингредиент: {str(e)}')

    def remove_ingredient(self):
        current_row = self.recipe_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите ингредиент для удаления')
            return
        
        recipe_id = int(self.recipe_table.item(current_row, 0).text())
        ingredient_name = self.recipe_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            f'Удалить "{ingredient_name}" из рецепта?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                with get_db() as db:
                    repo = RecipeRepository(db)
                    if repo.delete_recipe_item(recipe_id):
                        # Обновляем доступность блюда
                        repo.update_menu_item_availability(self.menu_item_id)
                        self.load_recipe()
                        QMessageBox.information(self, 'Успех', 'Ингредиент удален')
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Ингредиент не найден')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить ингредиент: {str(e)}')

# Добавляем импорт QGroupBox в начале файла
from PyQt5.QtWidgets import QGroupBox