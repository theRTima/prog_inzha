import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem,
                             QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox,
                             QSpinBox, QDoubleSpinBox, QDateEdit, QGroupBox,
                             QFormLayout, QHeaderView, QMessageBox, QSplitter,
                             QCheckBox, QDateTimeEdit)
from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtGui import QFont, QIcon


class RestaurantOrderSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Информационная система ресторана - Заказы навынос')
        self.setGeometry(100, 100, 1200, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Заголовок
        title_label = QLabel('Система управления заказами навынос')
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Создаем вкладки
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # Вкладка заказов
        self.create_orders_tab(tab_widget)

        # Вкладка меню
        self.create_menu_tab(tab_widget)

        # Вкладка инвентаря
        self.create_inventory_tab(tab_widget)

        # Вкладка отчетов
        self.create_reports_tab(tab_widget)

        # Статус бар
        self.statusBar().showMessage('Готов к работе')

    def create_orders_tab(self, tab_widget):
        """Создает вкладку для управления заказами навынос"""
        orders_tab = QWidget()
        layout = QVBoxLayout(orders_tab)

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

        splitter = QSplitter(Qt.Horizontal)

        # Таблица активных заказов
        orders_group = QGroupBox('Активные заказы')
        orders_layout = QVBoxLayout(orders_group)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels([
            'ID', 'Клиент', 'Телефон', 'Сумма', 'Статус', 'Время заказа'
        ])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.populate_sample_orders()

        orders_layout.addWidget(self.orders_table)
        splitter.addWidget(orders_group)

        order_details_group = QGroupBox('Детали заказа')
        order_details_layout = QVBoxLayout(order_details_group)

        # Форма деталей заказа
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
        tab_widget.addTab(orders_tab, 'Заказы')

        btn_new_order.clicked.connect(self.new_order)
        self.orders_table.itemSelectionChanged.connect(self.on_order_selected)

    def create_menu_tab(self, tab_widget):
        """Создает вкладку для управления меню"""
        menu_tab = QWidget()
        layout = QVBoxLayout(menu_tab)

        # Верхняя панель
        top_panel = QHBoxLayout()

        btn_add_dish = QPushButton('Добавить блюдо')
        btn_edit_dish = QPushButton('Редактировать')
        btn_delete_dish = QPushButton('Удалить')
        self.menu_filter = QComboBox()
        self.menu_filter.addItems(['Все категории', 'Горячие блюда', 'Салаты', 'Супы', 'Десерты', 'Напитки'])

        top_panel.addWidget(btn_add_dish)
        top_panel.addWidget(btn_edit_dish)
        top_panel.addWidget(btn_delete_dish)
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
        self.menu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.populate_sample_menu()

        layout.addWidget(self.menu_table)
        tab_widget.addTab(menu_tab, 'Меню')

    def create_inventory_tab(self, tab_widget):
        """Создает вкладку для учета инвентаря"""
        inventory_tab = QWidget()
        layout = QVBoxLayout(inventory_tab)

        # Верхняя панель
        top_panel = QHBoxLayout()

        btn_add_item = QPushButton('Добавить ингредиент')
        btn_edit_item = QPushButton('Редактировать')
        btn_update_stock = QPushButton('Обновить остатки')
        btn_low_stock = QPushButton('Низкие остатки')

        top_panel.addWidget(btn_add_item)
        top_panel.addWidget(btn_edit_item)
        top_panel.addWidget(btn_update_stock)
        top_panel.addWidget(btn_low_stock)
        top_panel.addStretch()

        layout.addLayout(top_panel)

        # Таблица инвентаря
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(7)
        self.inventory_table.setHorizontalHeaderLabels([
            'ID', 'Название', 'Категория', 'Ед. изм.', 'Текущий остаток', 'Минимум', 'Поставщик'
        ])
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.populate_sample_inventory()

        layout.addWidget(self.inventory_table)
        tab_widget.addTab(inventory_tab, 'Инвентарь')

    def create_reports_tab(self, tab_widget):
        """Создает вкладку для отчетов"""
        reports_tab = QWidget()
        layout = QVBoxLayout(reports_tab)

        # Панель управления отчетами
        control_panel = QHBoxLayout()

        self.report_type = QComboBox()
        self.report_type.addItems([
            'Отчет по продажам',
            'Отчет по остаткам',
            'Отчет по заказам',
            'Финансовый отчет',
            'Популярные блюда'
        ])

        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-7))
        self.date_from.setCalendarPopup(True)

        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)

        btn_generate = QPushButton('Сгенерировать отчет')
        btn_export = QPushButton('Экспорт в Excel')

        control_panel.addWidget(QLabel('Тип отчета:'))
        control_panel.addWidget(self.report_type)
        control_panel.addWidget(QLabel('С:'))
        control_panel.addWidget(self.date_from)
        control_panel.addWidget(QLabel('По:'))
        control_panel.addWidget(self.date_to)
        control_panel.addWidget(btn_generate)
        control_panel.addWidget(btn_export)
        control_panel.addStretch()

        layout.addLayout(control_panel)

        # Область для отчета
        self.report_text = QTextEdit()
        self.report_text.setPlaceholderText('Здесь будет отображаться сгенерированный отчет...')
        layout.addWidget(self.report_text)

        tab_widget.addTab(reports_tab, 'Отчеты')

    def populate_sample_orders(self):
        """Заполняет таблицу заказов тестовыми данными"""
        sample_orders = [
            ['ORD001', 'Иван Петров', '+7 (912) 345-67-89', '2500 руб.', 'Новый', '2024-01-15 12:30'],
            ['ORD002', 'Мария Сидорова', '+7 (923) 456-78-90', '1800 руб.', 'Готовится', '2024-01-15 12:45'],
            ['ORD003', 'Алексей Иванов', '+7 (934) 567-89-01', '3200 руб.', 'Готов к выдаче', '2024-01-15 13:00'],
            ['ORD004', 'Екатерина Смирнова', '+7 (945) 678-90-12', '1500 руб.', 'Выдан', '2024-01-15 11:20']
        ]

        self.orders_table.setRowCount(len(sample_orders))
        for row, order in enumerate(sample_orders):
            for col, data in enumerate(order):
                self.orders_table.setItem(row, col, QTableWidgetItem(str(data)))

    def populate_sample_menu(self):
        """Заполняет таблицу меню тестовыми данными"""
        sample_menu = [
            ['001', 'Стейк Рибай', 'Горячие блюда', '1200 руб.', 'Да', 'Стейк с картофелем'],
            ['002', 'Цезарь с курицей', 'Салаты', '450 руб.', 'Да', 'Салат Цезарь с куриной грудкой'],
            ['003', 'Томатный суп', 'Супы', '350 руб.', 'Да', 'Томатный суп с базиликом'],
            ['004', 'Тирамису', 'Десерты', '400 руб.', 'Нет', 'Классический тирамису'],
            ['005', 'Кофе латте', 'Напитки', '250 руб.', 'Да', 'Кофе латте 300 мл'],
            ['006', 'Бургер', 'Горячие блюда', '600 руб.', 'Да', 'Бургер с говядиной']
        ]

        self.menu_table.setRowCount(len(sample_menu))
        for row, dish in enumerate(sample_menu):
            for col, data in enumerate(dish):
                self.menu_table.setItem(row, col, QTableWidgetItem(str(data)))

    def populate_sample_inventory(self):
        """Заполняет таблицу инвентаря тестовыми данными"""
        sample_inventory = [
            ['001', 'Говядина', 'Мясо', 'кг', '15.5', '5.0', 'Мясной двор'],
            ['002', 'Куриное филе', 'Мясо', 'кг', '8.2', '3.0', 'Птицефабрика'],
            ['003', 'Помидоры', 'Овощи', 'кг', '12.0', '4.0', 'Овощная база'],
            ['004', 'Сыр пармезан', 'Молочные', 'кг', '2.5', '1.0', 'Сыроварня'],
            ['005', 'Кофе зерновой', 'Бакалея', 'кг', '5.0', '2.0', 'Кофейная компания'],
            ['006', 'Салат Айсберг', 'Овощи', 'кг', '3.2', '2.0', 'Овощная база']
        ]

        self.inventory_table.setRowCount(len(sample_inventory))
        for row, item in enumerate(sample_inventory):
            for col, data in enumerate(item):
                self.inventory_table.setItem(row, col, QTableWidgetItem(str(data)))

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

        self.statusBar().showMessage('Создание нового заказа навынос...')

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

            self.statusBar().showMessage(f'Выбран заказ {order_id}')


class DateTimeEdit(QDateTimeEdit):
    """Кастомный виджет для отображения даты и времени"""

    def __init__(self):
        super().__init__()
        self.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.setDateTime(QDateTime.currentDateTime())


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = RestaurantOrderSystem()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()