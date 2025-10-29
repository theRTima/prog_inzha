from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QComboBox, 
                             QMessageBox)
from PyQt5.QtCore import Qt
from config.database import get_db
from repositories.inventory_repository import InventoryRepository
from widgets.inventory_edit_dialog import InventoryEditDialog

class InventoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_inventory()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Верхняя панель
        top_panel = QHBoxLayout()

        btn_add_item = QPushButton('Добавить материал')
        btn_edit_item = QPushButton('Редактировать')
        btn_delete_item = QPushButton('Удалить')
        btn_low_stock = QPushButton('Низкие остатки')

        top_panel.addWidget(btn_add_item)
        top_panel.addWidget(btn_edit_item)
        top_panel.addWidget(btn_delete_item)
        top_panel.addWidget(btn_low_stock)
        top_panel.addStretch()

        layout.addLayout(top_panel)

        # Таблица инвентаря
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(7)
        self.inventory_table.setHorizontalHeaderLabels([
            'ID', 'Название', 'Категория', 'Ед. изм.', 'Текущий остаток', 'Минимум', 'Поставщик'
        ])
        self.inventory_table.setSortingEnabled(True)

        layout.addWidget(self.inventory_table)

        # Подключение сигналов
        btn_add_item.clicked.connect(self.add_inventory_item)
        btn_edit_item.clicked.connect(self.edit_inventory_item)
        btn_delete_item.clicked.connect(self.delete_inventory_item)
        btn_low_stock.clicked.connect(self.show_low_stock)

    def load_inventory(self):
        try:
            # Сохраняем сортировку
            sort_column = self.inventory_table.horizontalHeader().sortIndicatorSection()
            sort_order = self.inventory_table.horizontalHeader().sortIndicatorOrder()
            
            self.inventory_table.setSortingEnabled(False)
            
            with get_db() as db:
                repo = InventoryRepository(db)
                inventory_items = repo.get_all_inventory()
                
                self.inventory_table.setRowCount(len(inventory_items))
                for row, item in enumerate(inventory_items):
                    self.inventory_table.setItem(row, 0, QTableWidgetItem(str(item.id)))
                    self.inventory_table.setItem(row, 1, QTableWidgetItem(item.name))
                    self.inventory_table.setItem(row, 2, QTableWidgetItem(item.category))
                    self.inventory_table.setItem(row, 3, QTableWidgetItem(item.unit))
                    self.inventory_table.setItem(row, 4, QTableWidgetItem(str(item.current_stock)))
                    self.inventory_table.setItem(row, 5, QTableWidgetItem(str(item.min_stock)))
                    self.inventory_table.setItem(row, 6, QTableWidgetItem(item.supplier))
            
            self.inventory_table.setSortingEnabled(True)
            # Восстанавливаем сортировку
            self.inventory_table.sortByColumn(sort_column, sort_order)
            
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось загрузить инвентарь: {str(e)}')

    def add_inventory_item(self):
        dialog = InventoryEditDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            inventory_data = dialog.get_inventory_data()
            try:
                with get_db() as db:
                    repo = InventoryRepository(db)
                    repo.create_inventory_item(
                        name=inventory_data['name'],
                        category=inventory_data['category'],
                        unit=inventory_data['unit'],
                        current_stock=inventory_data['current_stock'],
                        min_stock=inventory_data['min_stock'],
                        supplier=inventory_data['supplier']
                    )
                self.load_inventory()
                QMessageBox.information(self, 'Успех', 'Материал добавлен в инвентарь')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить материал: {str(e)}')

    def edit_inventory_item(self):
        current_row = self.inventory_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите материал для редактирования')
            return
        
        item_id = int(self.inventory_table.item(current_row, 0).text())
        item_name = self.inventory_table.item(current_row, 1).text()
        item_category = self.inventory_table.item(current_row, 2).text()
        item_unit = self.inventory_table.item(current_row, 3).text()
        item_current_stock = float(self.inventory_table.item(current_row, 4).text())
        item_min_stock = float(self.inventory_table.item(current_row, 5).text())
        item_supplier = self.inventory_table.item(current_row, 6).text()
        
        inventory_data = {
            'name': item_name,
            'category': item_category,
            'unit': item_unit,
            'current_stock': item_current_stock,
            'min_stock': item_min_stock,
            'supplier': item_supplier
        }
        
        dialog = InventoryEditDialog(self, inventory_data)
        if dialog.exec_() == QDialog.Accepted:
            new_inventory_data = dialog.get_inventory_data()
            try:
                with get_db() as db:
                    repo = InventoryRepository(db)
                    updated_item = repo.update_inventory_item(item_id, **new_inventory_data)
                    if updated_item:
                        self.load_inventory()
                        QMessageBox.information(self, 'Успех', 'Материал обновлен')
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Материал не найден')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось обновить материал: {str(e)}')

    def delete_inventory_item(self):
        current_row = self.inventory_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите материал для удаления')
            return
        
        item_id = int(self.inventory_table.item(current_row, 0).text())
        item_name = self.inventory_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            f'Вы уверены, что хотите удалить материал "{item_name}"?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                with get_db() as db:
                    repo = InventoryRepository(db)
                    if repo.delete_inventory_item(item_id):
                        QMessageBox.information(self, 'Успех', 'Материал удален')
                        self.load_inventory()
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Материал не найден')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить материал: {str(e)}')

    def show_low_stock(self):
        try:
            with get_db() as db:
                repo = InventoryRepository(db)
                low_stock_items = repo.get_low_stock_items()
                
                if not low_stock_items:
                    QMessageBox.information(self, 'Информация', 'Нет материалов с низкими остатками')
                    return
                
                # Создаем временную таблицу для отображения
                low_stock_table = QTableWidget()
                low_stock_table.setColumnCount(4)
                low_stock_table.setHorizontalHeaderLabels([
                    'Название', 'Текущий остаток', 'Минимум', 'Разница'
                ])
                
                low_stock_table.setRowCount(len(low_stock_items))
                for row, item in enumerate(low_stock_items):
                    low_stock_table.setItem(row, 0, QTableWidgetItem(item.name))
                    low_stock_table.setItem(row, 1, QTableWidgetItem(str(item.current_stock)))
                    low_stock_table.setItem(row, 2, QTableWidgetItem(str(item.min_stock)))
                    low_stock_table.setItem(row, 3, QTableWidgetItem(str(item.min_stock - item.current_stock)))
                
                # Показываем диалог с таблицей
                dialog = QDialog(self)
                dialog.setWindowTitle('Материалы с низкими остатками')
                dialog.resize(500, 300)
                layout = QVBoxLayout(dialog)
                layout.addWidget(low_stock_table)
                
                button_box = QDialogButtonBox(QDialogButtonBox.Ok)
                button_box.accepted.connect(dialog.accept)
                layout.addWidget(button_box)
                
                dialog.exec_()
                
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось загрузить данные: {str(e)}')