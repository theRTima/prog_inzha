from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QComboBox, 
                             QMessageBox, QDialog, QSplitter, QGroupBox)
from PyQt5.QtCore import Qt

from config.database import get_db
from repositories.menu_repository import MenuRepository
from repositories.recipe_repository import RecipeRepository
from widgets.dish_edit_dialog import DishEditDialog
from widgets.recipe_edit_dialog import RecipeEditDialog

class NumericTableWidgetItem(QTableWidgetItem):
    """Элемент таблицы для числовой сортировки"""
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return super().__lt__(other)

class MenuTab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_dish_id = None
        self.initUI()
        self.load_menu_items()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Верхняя панель
        top_panel = QHBoxLayout()

        btn_add_dish = QPushButton('Добавить блюдо')
        btn_edit_dish = QPushButton('Редактировать')
        btn_edit_recipe = QPushButton('Редактировать рецепт')
        btn_delete_dish = QPushButton('Удалить')
        self.menu_filter = QComboBox()
        self.menu_filter.addItems(['Все категории', 'Горячие блюда', 'Салаты', 'Супы', 'Десерты', 'Напитки'])

        top_panel.addWidget(btn_add_dish)
        top_panel.addWidget(btn_edit_dish)
        top_panel.addWidget(btn_edit_recipe)
        top_panel.addWidget(btn_delete_dish)
        top_panel.addStretch()
        top_panel.addWidget(QLabel('Фильтр:'))
        top_panel.addWidget(self.menu_filter)

        main_layout.addLayout(top_panel)

        # Сплиттер для разделения меню и рецепта
        splitter = QSplitter(Qt.Vertical)

        # Верхняя часть - меню
        menu_group = QGroupBox('Меню')
        menu_layout = QVBoxLayout(menu_group)
        
        self.menu_table = QTableWidget()
        self.menu_table.setColumnCount(6)
        self.menu_table.setHorizontalHeaderLabels([
            'ID', 'Название', 'Категория', 'Цена', 'Доступно', 'Описание'
        ])
        self.menu_table.setSortingEnabled(True)
        menu_layout.addWidget(self.menu_table)
        
        splitter.addWidget(menu_group)

        # Нижняя часть - рецепт выбранного блюда
        recipe_group = QGroupBox('Рецепт выбранного блюда')
        recipe_layout = QVBoxLayout(recipe_group)
        
        self.recipe_table = QTableWidget()
        self.recipe_table.setColumnCount(5)
        self.recipe_table.setHorizontalHeaderLabels([
            'Ингредиент', 'Количество', 'Ед. изм.', 'Текущий остаток', 'Достаточно'
        ])
        self.recipe_table.setSortingEnabled(True)
        recipe_layout.addWidget(self.recipe_table)
        
        splitter.addWidget(recipe_group)
        
        # Устанавливаем начальные размеры
        splitter.setSizes([300, 200])

        main_layout.addWidget(splitter)

        # Подключение сигналов
        btn_add_dish.clicked.connect(self.add_dish)
        btn_edit_dish.clicked.connect(self.edit_dish)
        btn_edit_recipe.clicked.connect(self.open_recipe_editor)
        btn_delete_dish.clicked.connect(self.delete_dish)
        self.menu_filter.currentTextChanged.connect(self.load_menu_items)
        self.menu_table.itemSelectionChanged.connect(self.load_selected_recipe)

    def load_menu_items(self):
        """Загружает блюда из базы данных с учетом фильтра"""
        try:
            sort_column = self.menu_table.horizontalHeader().sortIndicatorSection()
            sort_order = self.menu_table.horizontalHeader().sortIndicatorOrder()
            
            self.menu_table.setSortingEnabled(False)
            
            with get_db() as db:
                repo = MenuRepository(db)
                category = self.menu_filter.currentText()
                
                if category == 'Все категории':
                    menu_items = repo.get_all_menu_items()
                else:
                    menu_items = repo.get_menu_items_by_category(category)
                
                self.menu_table.setRowCount(len(menu_items))
                for row, item in enumerate(menu_items):
                    self.menu_table.setItem(row, 0, NumericTableWidgetItem(str(item.id)))
                    self.menu_table.setItem(row, 1, QTableWidgetItem(item.name))
                    self.menu_table.setItem(row, 2, QTableWidgetItem(item.category))
                    self.menu_table.setItem(row, 3, NumericTableWidgetItem(str(item.price)))
                    self.menu_table.setItem(row, 4, QTableWidgetItem('Да' if item.available else 'Нет'))
                    self.menu_table.setItem(row, 5, QTableWidgetItem(item.description or ''))
            
            self.menu_table.setSortingEnabled(True)
            self.menu_table.sortByColumn(sort_column, sort_order)
            
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось загрузить меню: {str(e)}')

    def load_selected_recipe(self):
        """Загружает рецепт выбранного блюда"""
        selected = self.menu_table.selectedIndexes()
        if not selected:
            return
        
        internal_row = selected[0].row()
        item = self.menu_table.item(internal_row, 0)
        if not item:
            return
        
        try:
            menu_item_id = int(item.text())
            self.current_dish_id = menu_item_id
            
            with get_db() as db:
                recipe_repo = RecipeRepository(db)
                recipe_items = recipe_repo.get_recipe_for_menu_item(menu_item_id)
                
                self.recipe_table.setRowCount(len(recipe_items))
                for row, recipe_item in enumerate(recipe_items):
                    inventory_item = recipe_item.inventory_item
                    required = recipe_item.quantity_required
                    available = inventory_item.current_stock
                    enough = available >= required
                    
                    self.recipe_table.setItem(row, 0, QTableWidgetItem(inventory_item.name))
                    self.recipe_table.setItem(row, 1, NumericTableWidgetItem(str(required)))
                    self.recipe_table.setItem(row, 2, QTableWidgetItem(inventory_item.unit))
                    self.recipe_table.setItem(row, 3, NumericTableWidgetItem(str(available)))
                    self.recipe_table.setItem(row, 4, QTableWidgetItem('Да' if enough else 'Нет'))
                    
        except Exception as e:
            print(f"Ошибка загрузки рецепта: {e}")
            self.recipe_table.setRowCount(0)

    def add_dish(self):
        """Добавление нового блюда"""
        dialog = DishEditDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            dish_data = dialog.get_dish_data()
            try:
                with get_db() as db:
                    repo = MenuRepository(db)
                    repo.create_menu_item(
                        name=dish_data['name'],
                        category=dish_data['category'],
                        price=dish_data['price'],
                        available=dish_data['available'],
                        description=dish_data['description']
                    )
                self.load_menu_items()
                QMessageBox.information(self, 'Успех', 'Блюдо добавлено в меню')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить блюдо: {str(e)}')

    def edit_dish(self):
        """Редактирование выбранного блюда"""
        selected = self.menu_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите блюдо для редактирования')
            return
        
        internal_row = selected[0].row()
        
        dish_id_item = self.menu_table.item(internal_row, 0)
        dish_name_item = self.menu_table.item(internal_row, 1)
        dish_category_item = self.menu_table.item(internal_row, 2)
        dish_price_item = self.menu_table.item(internal_row, 3)
        dish_available_item = self.menu_table.item(internal_row, 4)
        dish_description_item = self.menu_table.item(internal_row, 5)
        
        if not all([dish_id_item, dish_name_item, dish_category_item, dish_price_item, dish_available_item]):
            return
        
        dish_id = int(dish_id_item.text())
        dish_name = dish_name_item.text()
        dish_category = dish_category_item.text()
        dish_price = float(dish_price_item.text())
        dish_available = dish_available_item.text() == 'Да'
        dish_description = dish_description_item.text() if dish_description_item else ''
        
        dish_data = {
            'name': dish_name,
            'category': dish_category,
            'price': dish_price,
            'available': dish_available,
            'description': dish_description
        }
        
        dialog = DishEditDialog(self, dish_data)
        if dialog.exec_() == QDialog.Accepted:
            new_dish_data = dialog.get_dish_data()
            try:
                with get_db() as db:
                    repo = MenuRepository(db)
                    updated_item = repo.update_menu_item(
                        dish_id,
                        name=new_dish_data['name'],
                        category=new_dish_data['category'],
                        price=new_dish_data['price'],
                        available=new_dish_data['available'],
                        description=new_dish_data['description']
                    )
                    
                    if updated_item:
                        self.load_menu_items()
                        QMessageBox.information(self, 'Успех', 'Блюдо обновлено')
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Блюдо не найдено')
                        
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось обновить блюдо: {str(e)}')

    def delete_dish(self):
        """Удаление выбранного блюда"""
        selected = self.menu_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите блюдо для удаления')
            return
        
        internal_row = selected[0].row()
        dish_id_item = self.menu_table.item(internal_row, 0)
        dish_name_item = self.menu_table.item(internal_row, 1)
        
        if not dish_id_item or not dish_name_item:
            return
        
        dish_id = int(dish_id_item.text())
        dish_name = dish_name_item.text()
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            f'Вы уверены, что хотите удалить блюдо "{dish_name}"?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                with get_db() as db:
                    repo = MenuRepository(db)
                    if repo.delete_menu_item(dish_id):
                        QMessageBox.information(self, 'Успех', 'Блюдо удалено')
                        self.load_menu_items()
                        self.recipe_table.setRowCount(0)
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Блюдо не найдено')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить блюдо: {str(e)}')
    
    def open_recipe_editor(self):
        """Открывает диалог редактирования рецепта для выбранного блюда"""
        selected = self.menu_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите блюдо для редактирования рецепта')
            return
        
        internal_row = selected[0].row()
        menu_item_id_item = self.menu_table.item(internal_row, 0)
        menu_item_name_item = self.menu_table.item(internal_row, 1)
        
        if not menu_item_id_item or not menu_item_name_item:
            return
        
        menu_item_id = int(menu_item_id_item.text())
        menu_item_name = menu_item_name_item.text()
        
        dialog = RecipeEditDialog(self, menu_item_id, menu_item_name)
        if dialog.exec_() == QDialog.Accepted:
            self.load_selected_recipe()
            self.load_menu_items()

    def refresh_menu(self):
        """Публичный метод для обновления данных извне"""
        self.load_menu_items()
        self.load_selected_recipe()