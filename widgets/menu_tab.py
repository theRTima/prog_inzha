from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QComboBox, 
                             QMessageBox, QDialog)
from PyQt5.QtCore import Qt

from config.database import get_db
from repositories.menu_repository import MenuRepository
from widgets.dish_edit_dialog import DishEditDialog
from widgets.recipe_edit_dialog import RecipeEditDialog

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
        btn_view_recipe = QPushButton('Рецепт')
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
            # Сохраняем сортировку
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
                    self.menu_table.setItem(row, 0, QTableWidgetItem(str(item.id)))
                    self.menu_table.setItem(row, 1, QTableWidgetItem(item.name))
                    self.menu_table.setItem(row, 2, QTableWidgetItem(item.category))
                    self.menu_table.setItem(row, 3, QTableWidgetItem(str(item.price)))
                    self.menu_table.setItem(row, 4, QTableWidgetItem('Да' if item.available else 'Нет'))
                    self.menu_table.setItem(row, 5, QTableWidgetItem(item.description or ''))
            
            self.menu_table.setSortingEnabled(True)
            # Восстанавливаем сортировку
            self.menu_table.sortByColumn(sort_column, sort_order)
            
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось загрузить меню: {str(e)}')

    def add_dish(self):
        """Добавление нового блюда"""
        dialog = DishEditDialog(self)
        if dialog.exec_() == DishEditDialog.Accepted:
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
        current_row = self.menu_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите блюдо для редактирования')
            return
        
        dish_id = int(self.menu_table.item(current_row, 0).text())
        dish_name = self.menu_table.item(current_row, 1).text()
        dish_category = self.menu_table.item(current_row, 2).text()
        dish_price = float(self.menu_table.item(current_row, 3).text())
        dish_available = self.menu_table.item(current_row, 4).text() == 'Да'
        dish_description = self.menu_table.item(current_row, 5).text()
        
        dish_data = {
            'name': dish_name,
            'category': dish_category,
            'price': dish_price,
            'available': dish_available,
            'description': dish_description
        }
        
        dialog = DishEditDialog(self, dish_data)
        if dialog.exec_() == QDialog.Accepted:  # Убедитесь, что используете QDialog.Accepted
            new_dish_data = dialog.get_dish_data()
            try:
                with get_db() as db:
                    repo = MenuRepository(db)
                    # ВЫЗЫВАЕМ МЕТОД ОБНОВЛЕНИЯ
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
        current_row = self.menu_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите блюдо для удаления')
            return
        
        dish_id = int(self.menu_table.item(current_row, 0).text())
        dish_name = self.menu_table.item(current_row, 1).text()
        
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
        current_row = self.menu_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите блюдо для просмотра рецепта')
            return
        
        menu_item_id = int(self.menu_table.item(current_row, 0).text())
        menu_item_name = self.menu_table.item(current_row, 1).text()
        
        dialog = RecipeEditDialog(self, menu_item_id, menu_item_name)
        dialog.exec_()
        # После закрытия диалога обновляем таблицу меню
        self.load_menu_items()