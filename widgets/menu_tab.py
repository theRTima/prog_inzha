from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QComboBox, 
                             QMessageBox, QDialog)
from PyQt5.QtCore import Qt

from config.database import get_db
from repositories.menu_repository import MenuRepository
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
        self.initUI()
        self.load_menu_items()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Верхняя панель
        top_panel = QHBoxLayout()

        btn_add_dish = QPushButton('Добавить блюдо')
        btn_edit_dish = QPushButton('Редактировать')
        btn_delete_dish = QPushButton('Удалить')
        btn_view_recipe = QPushButton('Технологическая карта')
        self.menu_filter = QComboBox()
        self.menu_filter.addItems(['Все категории', 'Горячие блюда', 'Салаты', 'Супы', 'Десерты', 'Напитки'])

        top_panel.addWidget(btn_add_dish)
        top_panel.addWidget(btn_edit_dish)
        top_panel.addWidget(btn_delete_dish)
        top_panel.addWidget(btn_view_recipe)
        top_panel.addStretch()
        top_panel.addWidget(QLabel('Фильтр:'))
        top_panel.addWidget(self.menu_filter)

        layout.addLayout(top_panel)

        # Таблица меню
        self.menu_table = QTableWidget()
        self.menu_table.setColumnCount(6)
        self.menu_table.setHorizontalHeaderLabels([
            'ID', 'Название', 'Категория', 'Цена', 'Доступно', 'Описание'
        ])
        self.menu_table.setSortingEnabled(True)

        layout.addWidget(self.menu_table)

        # Подключение сигналов
        btn_add_dish.clicked.connect(self.add_dish)
        btn_edit_dish.clicked.connect(self.edit_dish)
        btn_delete_dish.clicked.connect(self.delete_dish)
        btn_view_recipe.clicked.connect(self.view_recipe)
        self.menu_filter.currentTextChanged.connect(self.load_menu_items)

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
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Блюдо не найдено')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить блюдо: {str(e)}')
    
    def view_recipe(self):
        selected = self.menu_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите блюдо для просмотра рецепта')
            return
        
        internal_row = selected[0].row()
        menu_item_id_item = self.menu_table.item(internal_row, 0)
        menu_item_name_item = self.menu_table.item(internal_row, 1)
        
        if not menu_item_id_item or not menu_item_name_item:
            return
        
        menu_item_id = int(menu_item_id_item.text())
        menu_item_name = menu_item_name_item.text()
        
        dialog = RecipeEditDialog(self, menu_item_id, menu_item_name)
        dialog.exec_()
        self.load_menu_items()