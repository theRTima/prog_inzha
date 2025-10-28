from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QComboBox)

class MenuTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

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

        self.populate_sample_menu()
        layout.addWidget(self.menu_table)

    def populate_sample_menu(self):
        """Заполняет таблицу меню тестовыми данными"""
        sample_menu = [
            ['001', 'Стейк Рибай', 'Горячие блюда', '1200 руб.', 'Да', 'Стейк с картофелем'],
            ['002', 'Цезарь с курицей', 'Салаты', '450 руб.', 'Да', 'Салат Цезарь с куриной грудкой'],
            ['003', 'Томатный суп', 'Супы', '350 руб.', 'Да', 'Томатный суп с базиликом'],
            ['004', 'Тирамису', 'Десерты', '400 руб.', 'Нет', 'Классический тирамису'],
        ]

        self.menu_table.setRowCount(len(sample_menu))
        for row, dish in enumerate(sample_menu):
            for col, data in enumerate(dish):
                self.menu_table.setItem(row, col, QTableWidgetItem(str(data)))