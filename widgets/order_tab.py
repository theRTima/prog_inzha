from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QComboBox, QDateTimeEdit, QGroupBox, 
                             QFormLayout, QSplitter, QMessageBox, QDialog)
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QFont
from config.database import get_db
from repositories.order_repository import OrderRepository
from repositories.menu_repository import MenuRepository
from widgets.dish_selection_dialog import DishSelectionDialog

class NumericTableWidgetItem(QTableWidgetItem):
    """Элемент таблицы для числовой сортировки"""
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return super().__lt__(other)

class OrderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_order_id = None
        self.initUI()
        self.load_orders_from_db()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Верхняя панель с кнопками
        top_panel = QHBoxLayout()

        self.btn_new_order = QPushButton('Новый заказ')
        self.btn_save_order = QPushButton('Сохранить заказ')
        self.btn_delete_order = QPushButton('Удалить заказ')
        btn_complete_order = QPushButton('Завершить заказ')
        btn_print_receipt = QPushButton('Печать чека')

        top_panel.addWidget(self.btn_new_order)
        top_panel.addWidget(self.btn_save_order)
        top_panel.addWidget(self.btn_delete_order)
        top_panel.addWidget(btn_complete_order)
        top_panel.addWidget(btn_print_receipt)
        top_panel.addStretch()

        layout.addLayout(top_panel)

        splitter = QSplitter()

        # Таблица активных заказов
        orders_group = QGroupBox('Активные заказы')
        orders_layout = QVBoxLayout(orders_group)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels([
            'ID', 'Клиент', 'Телефон', 'Сумма', 'Статус', 'Время заказа'
        ])
        self.orders_table.setSortingEnabled(True)

        orders_layout.addWidget(self.orders_table)
        splitter.addWidget(orders_group)

        # Детали заказа
        order_details_group = QGroupBox('Детали заказа')
        order_details_layout = QVBoxLayout(order_details_group)

        details_form = QFormLayout()

        self.order_id = QLineEdit()
        self.order_id.setReadOnly(True)
        self.order_customer = QLineEdit()
        self.order_phone = QLineEdit()
        self.order_status = QComboBox()
        self.order_status.addItems(['Новый', 'Подтвержден', 'Готовится', 'Готов к выдаче', 'Выдан', 'Отменен'])
        self.order_created = QDateTimeEdit()
        self.order_created.setDateTime(QDateTime.currentDateTime())
        self.order_created.setCalendarPopup(True)
        self.order_notes = QTextEdit()
        self.order_notes.setMaximumHeight(60)
        self.order_notes.setPlaceholderText('Примечания к заказу...')

        details_form.addRow('ID заказа:', self.order_id)
        details_form.addRow('Имя клиента:', self.order_customer)
        details_form.addRow('Телефон:', self.order_phone)
        details_form.addRow('Статус:', self.order_status)
        details_form.addRow('Время заказа:', self.order_created)

        order_details_layout.addLayout(details_form)
        order_details_layout.addWidget(QLabel('Примечания:'))
        order_details_layout.addWidget(self.order_notes)

        # Таблица позиций заказа
        self.order_items_table = QTableWidget()
        self.order_items_table.setColumnCount(5)
        self.order_items_table.setHorizontalHeaderLabels([
            'ID', 'Блюдо', 'Количество', 'Цена', 'Сумма'
        ])
        self.order_items_table.setSortingEnabled(True)
        order_details_layout.addWidget(QLabel('Позиции заказа:'))
        order_details_layout.addWidget(self.order_items_table)

        # Панель управления позициями заказа
        items_panel = QHBoxLayout()
        btn_add_item = QPushButton('Добавить блюдо')
        btn_remove_item = QPushButton('Удалить блюдо')
        items_panel.addWidget(btn_add_item)
        items_panel.addWidget(btn_remove_item)
        items_panel.addStretch()
        order_details_layout.addLayout(items_panel)

        self.order_total = QLabel('Итого: 0 руб.')
        self.order_total.setFont(QFont('Arial', 12, QFont.Bold))
        order_details_layout.addWidget(self.order_total)

        splitter.addWidget(order_details_group)
        splitter.setSizes([400, 400])

        layout.addWidget(splitter)

        # Подключение сигналов
        self.btn_new_order.clicked.connect(self.new_order)
        self.btn_save_order.clicked.connect(self.save_order)
        self.btn_delete_order.clicked.connect(self.delete_order)
        self.orders_table.itemSelectionChanged.connect(self.on_order_selected)

        btn_add_item.clicked.connect(self.add_dish_to_order)
        btn_remove_item.clicked.connect(self.remove_dish_from_order)

    def load_orders_from_db(self):
        """Загружает заказы из базы данных"""
        try:
            sort_column = self.orders_table.horizontalHeader().sortIndicatorSection()
            sort_order = self.orders_table.horizontalHeader().sortIndicatorOrder()
            self.orders_table.setSortingEnabled(False)
            
            with get_db() as db:
                repo = OrderRepository(db)
                orders = repo.get_all_orders()
                
                self.orders_table.setRowCount(len(orders))
                for row, order in enumerate(orders):
                    self.orders_table.setItem(row, 0, NumericTableWidgetItem(str(order.id)))
                    self.orders_table.setItem(row, 1, QTableWidgetItem(order.customer_name))
                    self.orders_table.setItem(row, 2, QTableWidgetItem(order.phone or ""))
                    self.orders_table.setItem(row, 3, NumericTableWidgetItem(str(order.total)))
                    self.orders_table.setItem(row, 4, QTableWidgetItem(order.status))
                    self.orders_table.setItem(row, 5, QTableWidgetItem(order.formatted_created))
            
            self.orders_table.setSortingEnabled(True)
            self.orders_table.sortByColumn(sort_column, sort_order)

        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось загрузить заказы: {str(e)}')

    def new_order(self):
        """Создание нового заказа"""
        self.current_order_id = None
        self.order_id.clear()
        self.order_customer.clear()
        self.order_phone.clear()
        self.order_status.setCurrentIndex(0)
        self.order_created.setDateTime(QDateTime.currentDateTime())
        self.order_notes.clear()
        self.order_items_table.setRowCount(0)
        self.order_total.setText('Итого: 0 руб.')

    def save_order(self):
        """Сохранение заказа в базу данных"""
        try:
            customer_name = self.order_customer.text().strip()
            if not customer_name:
                QMessageBox.warning(self, 'Ошибка', 'Введите имя клиента')
                return

            with get_db() as db:
                repo = OrderRepository(db)
                
                if self.current_order_id:
                    order = repo.update_order(
                        self.current_order_id,
                        customer_name=customer_name,
                        phone=self.order_phone.text(),
                        status=self.order_status.currentText(),
                        notes=self.order_notes.toPlainText()
                    )
                    if order:
                        QMessageBox.information(self, 'Успех', f'Заказ #{order.id} обновлен')
                else:
                    order = repo.create_order(
                        customer_name=customer_name,
                        phone=self.order_phone.text(),
                        notes=self.order_notes.toPlainText()
                    )
                    self.current_order_id = order.id
                    self.order_id.setText(str(order.id))
                    QMessageBox.information(self, 'Успех', f'Создан новый заказ #{order.id}')
                
                self.load_orders_from_db()
                
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить заказ: {str(e)}')

    def delete_order(self):
        """Удаление выбранного заказа"""
        selected = self.orders_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите заказ для удаления')
            return
        
        internal_row = selected[0].row()
        item = self.orders_table.item(internal_row, 0)
        if not item:
            return
        
        order_id = int(item.text())
        
        reply = QMessageBox.question(self, 'Подтверждение', 
                                   f'Вы уверены, что хотите удалить заказ #{order_id}?',
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                with get_db() as db:
                    repo = OrderRepository(db)
                    if repo.delete_order(order_id):
                        QMessageBox.information(self, 'Успех', 'Заказ удален')
                        self.new_order()
                        self.load_orders_from_db()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить заказ: {str(e)}')

    def on_order_selected(self):
        """Обработчик выбора заказа в таблице"""
        selected = self.orders_table.selectedIndexes()
        if not selected:
            return
        
        internal_row = selected[0].row()
        item = self.orders_table.item(internal_row, 0)
        if not item:
            return
        
        try:
            order_id = int(item.text())
            self.current_order_id = order_id
            
            with get_db() as db:
                repo = OrderRepository(db)
                order = repo.get_order(order_id)
                
                if order:
                    self.order_id.setText(str(order.id))
                    self.order_customer.setText(order.customer_name)
                    self.order_phone.setText(order.phone or "")
                    self.order_notes.setPlainText(order.notes or "")
                    
                    index = self.order_status.findText(order.status)
                    if index >= 0:
                        self.order_status.setCurrentIndex(index)
                    
                    if order.created:
                        self.order_created.setDateTime(order.created)
                    
                    self.load_order_items(order_id)
                    
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось загрузить данные заказа: {str(e)}')

    def add_dish_to_order(self):
        """Добавление блюда в заказ"""
        if not self.current_order_id:
            QMessageBox.warning(self, 'Ошибка', 'Сначала создайте или выберите заказ')
            return
        
        dialog = DishSelectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            dish_data = dialog.get_selected_dish()
            if dish_data:
                try:
                    with get_db() as db:
                        repo = OrderRepository(db)
                        
                        # Проверяем доступность ингредиентов перед добавлением
                        from repositories.recipe_repository import RecipeRepository
                        recipe_repo = RecipeRepository(db)
                        
                        recipe_items = recipe_repo.get_recipe_for_menu_item(dish_data['id'])
                        for recipe_item in recipe_items:
                            required = recipe_item.quantity_required * dish_data['quantity']
                            if recipe_item.inventory_item.current_stock < required:
                                QMessageBox.warning(
                                    self, 'Недостаточно ингредиентов',
                                    f"Недостаточно '{recipe_item.inventory_item.name}' для блюда '{dish_data['name']}'. "
                                    f"Требуется: {required} {recipe_item.inventory_item.unit}, "
                                    f"доступно: {recipe_item.inventory_item.current_stock} {recipe_item.inventory_item.unit}"
                                )
                                return
                        
                        order_item = repo.add_order_item(
                            self.current_order_id,
                            dish_data['id'],
                            dish_data['quantity']
                        )
                        
                        self.load_order_items(self.current_order_id)
                        QMessageBox.information(self, 'Успех', 'Блюдо добавлено в заказ')
                        
                except Exception as e:
                    QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить блюдо: {str(e)}')

    def remove_dish_from_order(self):
        """Удаление блюда из заказа"""
        selected = self.order_items_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, 'Ошибка', 'Выберите позицию для удаления')
            return
        
        internal_row = selected[0].row()
        item = self.order_items_table.item(internal_row, 0)
        if not item:
            return
        
        order_item_id = int(item.text())
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            f'Удалить позицию #{order_item_id} из заказа?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                with get_db() as db:
                    repo = OrderRepository(db)
                    repo.remove_order_item(order_item_id)
                    self.load_order_items(self.current_order_id)
                    QMessageBox.information(self, 'Успех', 'Позиция удалена из заказа')
                    
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить позицию: {str(e)}')

    def load_order_items(self, order_id: int):
        """Загрузка позиций заказа"""
        try:
            with get_db() as db:
                repo = OrderRepository(db)
                order = repo.get_order(order_id)
                
                if order:
                    self.order_items_table.setSortingEnabled(False)
                    
                    self.order_items_table.setRowCount(len(order.items))
                    for row, item in enumerate(order.items):
                        dish_name = item.menu_item.name if item.menu_item else "Неизвестно"
                        item_total = item.quantity * item.price
                        
                        self.order_items_table.setItem(row, 0, NumericTableWidgetItem(str(item.id)))
                        self.order_items_table.setItem(row, 1, QTableWidgetItem(dish_name))
                        self.order_items_table.setItem(row, 2, NumericTableWidgetItem(str(item.quantity)))
                        self.order_items_table.setItem(row, 3, NumericTableWidgetItem(str(item.price)))
                        self.order_items_table.setItem(row, 4, NumericTableWidgetItem(str(item_total)))
                    
                    self.order_items_table.setSortingEnabled(True)
                    self.order_total.setText(f'Итого: {order.total} руб.')
                    
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось загрузить позиции заказа: {str(e)}')