from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QComboBox, QDateTimeEdit, QGroupBox, 
                             QFormLayout, QSplitter)
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QFont

class OrderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Верхняя панель с кнопками
        top_panel = QHBoxLayout()

        btn_new_order = QPushButton('Новый заказ')
        btn_edit_order = QPushButton('Редактировать')
        btn_complete_order = QPushButton('Завершить заказ')
        btn_cancel_order = QPushButton('Отменить заказ')
        btn_print_receipt = QPushButton('Печать чека')

        top_panel.addWidget(btn_new_order)
        top_panel.addWidget(btn_edit_order)
        top_panel.addWidget(btn_complete_order)
        top_panel.addWidget(btn_cancel_order)
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

        self.populate_sample_orders()
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
        btn_new_order.clicked.connect(self.new_order)
        self.orders_table.itemSelectionChanged.connect(self.on_order_selected)

    def populate_sample_orders(self):
        """Заполняет таблицу заказов тестовыми данными"""
        sample_orders = [
            ['ORD001', 'Иван Петров', '+7 (912) 345-67-89', '2500 руб.', 'Новый', '2024-01-15 12:30'],
            ['ORD002', 'Мария Сидорова', '+7 (923) 456-78-90', '1800 руб.', 'Готовится', '2024-01-15 12:45'],
            ['ORD003', 'Алексей Иванов', '+7 (934) 567-89-01', '3200 руб.', 'Готов к выдаче', '2024-01-15 13:00'],
        ]

        self.orders_table.setRowCount(len(sample_orders))
        for row, order in enumerate(sample_orders):
            for col, data in enumerate(order):
                self.orders_table.setItem(row, col, QTableWidgetItem(str(data)))

    def new_order(self):
        """Создание нового заказа"""
        self.order_id.clear()
        self.order_customer.clear()
        self.order_phone.clear()
        self.order_status.setCurrentIndex(0)
        self.order_created.setDateTime(QDateTime.currentDateTime())
        self.order_notes.clear()
        self.order_items_table.setRowCount(0)
        self.order_total.setText('Итого: 0 руб.')

    def on_order_selected(self):
        """Обработчик выбора заказа в таблице"""
        current_row = self.orders_table.currentRow()
        if current_row >= 0:
            order_id = self.orders_table.item(current_row, 0).text()
            customer = self.orders_table.item(current_row, 1).text()
            phone = self.orders_table.item(current_row, 2).text()
            status = self.orders_table.item(current_row, 4).text()

            self.order_id.setText(order_id)
            self.order_customer.setText(customer)
            self.order_phone.setText(phone)

            index = self.order_status.findText(status)
            if index >= 0:
                self.order_status.setCurrentIndex(index)