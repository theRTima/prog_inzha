from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QComboBox, QDateTimeEdit, QGroupBox, 
                             QFormLayout, QSplitter, QMessageBox)
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QFont
from config.database import get_db
from repositories.order_repository import OrderRepository

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
        self.order_items_table.setColumnCount(4)
        self.order_items_table.setHorizontalHeaderLabels([
            'Блюдо', 'Количество', 'Цена', 'Сумма'
        ])
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

    def load_orders_from_db(self):
        """Загружает заказы из базы данных"""
        try:
            with get_db() as db:
                repo = OrderRepository(db)
                orders = repo.get_all_orders()
                
                self.orders_table.setRowCount(len(orders))
                for row, order in enumerate(orders):
                    self.orders_table.setItem(row, 0, QTableWidgetItem(str(order.id)))
                    self.orders_table.setItem(row, 1, QTableWidgetItem(order.customer_name))
                    self.orders_table.setItem(row, 2, QTableWidgetItem(order.phone or ""))
                    self.orders_table.setItem(row, 3, QTableWidgetItem(str(order.total)))
                    self.orders_table.setItem(row, 4, QTableWidgetItem(order.status))
                    self.orders_table.setItem(row, 5, QTableWidgetItem(order.formatted_created()))
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
                    # Обновление существующего заказа
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
                    # Создание нового заказа
                    order = repo.create_order(
                        customer_name=customer_name,
                        phone=self.order_phone.text(),
                        notes=self.order_notes.toPlainText()
                    )
                    self.current_order_id = order.id
                    self.order_id.setText(str(order.id))
                    QMessageBox.information(self, 'Успех', f'Создан новый заказ #{order.id}')
                
                # Обновляем таблицу заказов
                self.load_orders_from_db()
                
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить заказ: {str(e)}')

    def delete_order(self):
        """Удаление выбранного заказа"""
        if not self.current_order_id:
            QMessageBox.warning(self, 'Ошибка', 'Выберите заказ для удаления')
            return
        
        reply = QMessageBox.question(self, 'Подтверждение', 
                                   f'Вы уверены, что хотите удалить заказ #{self.current_order_id}?',
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                with get_db() as db:
                    repo = OrderRepository(db)
                    if repo.delete_order(self.current_order_id):
                        QMessageBox.information(self, 'Успех', 'Заказ удален')
                        self.new_order()  # Очищаем форму
                        self.load_orders_from_db()  # Обновляем таблицу
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить заказ: {str(e)}')

    def on_order_selected(self):
        """Обработчик выбора заказа в таблице"""
        current_row = self.orders_table.currentRow()
        if current_row >= 0:
            try:
                order_id = int(self.orders_table.item(current_row, 0).text())
                self.current_order_id = order_id
                
                with get_db() as db:
                    repo = OrderRepository(db)
                    order = repo.get_order(order_id)
                    
                    if order:
                        self.order_id.setText(str(order.id))
                        self.order_customer.setText(order.customer_name)
                        self.order_phone.setText(order.phone or "")
                        self.order_notes.setPlainText(order.notes or "")
                        
                        # Устанавливаем статус
                        index = self.order_status.findText(order.status)
                        if index >= 0:
                            self.order_status.setCurrentIndex(index)
                        
                        # Устанавливаем время создания
                        if order.created:
                            self.order_created.setDateTime(order.created)
                        
                        # Обновляем итоговую сумму
                        self.order_total.setText(f'Итого: {order.total} руб.')
                        
                        # Загружаем позиции заказа
                        self.load_order_items(order)
                        
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Не удалось загрузить данные заказа: {str(e)}')

    def load_order_items(self, order):
        """Загружает позиции выбранного заказа"""
        self.order_items_table.setRowCount(len(order.items))
        for row, item in enumerate(order.items):
            dish_name = item.menu_item.name if item.menu_item else "Неизвестно"
            self.order_items_table.setItem(row, 0, QTableWidgetItem(dish_name))
            self.order_items_table.setItem(row, 1, QTableWidgetItem(str(item.quantity)))
            self.order_items_table.setItem(row, 2, QTableWidgetItem(str(item.price)))
            self.order_items_table.setItem(row, 3, QTableWidgetItem(str(item.quantity * item.price)))