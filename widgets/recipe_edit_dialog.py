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
        self.setWindowTitle(f'Рецепт: {self.menu_item_name}')
        self.setModal(True)
        self.resize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Таблица текущего рецепта
        layout.addWidget(QLabel('Ингредиенты:'))
        self.recipe_table = QTableWidget()
        self.recipe_table.setColumnCount(5)
        self.recipe_table.setHorizontalHeaderLabels([
            'ID', 'Ингредиент', 'Количество', 'Ед. изм.', 'Доступно'
        ])
        layout.addWidget(self.recipe_table)
        
        # Панель добавления нового ингредиента
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel('Добавить ингредиент:'))
        
        self.inventory_combo = QComboBox()
        add_layout.addWidget(self.inventory_combo)
        
        add_layout.addWidget(QLabel('Количество:'))
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setValidator(QDoubleValidator(0, 1000, 3, self))
        self.quantity_edit.setPlaceholderText("0.000")
        add_layout.addWidget(self.quantity_edit)
        
        btn_add = QPushButton('Добавить')
        btn_add.clicked.connect(self.add_ingredient)
        add_layout.addWidget(btn_add)
        
        add_layout.addStretch()
        layout.addLayout(add_layout)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        btn_remove = QPushButton('Удалить выбранный ингредиент')
        btn_remove.clicked.connect(self.remove_ingredient)
        button_layout.addWidget(btn_remove)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Кнопки закрытия
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
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
        
        try:
            quantity = float(quantity_text)
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректное количество')
            return
        
        try:
            with get_db() as db:
                repo = RecipeRepository(db)
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