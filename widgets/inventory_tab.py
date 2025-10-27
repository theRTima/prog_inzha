from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel)

class InventoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Весь код из create_inventory_tab
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

        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(7)
        self.inventory_table.setHorizontalHeaderLabels([
            'ID', 'Название', 'Категория', 'Ед. изм.', 'Текущий остаток', 'Минимум', 'Поставщик'
        ])

        self.populate_sample_inventory()
        layout.addWidget(self.inventory_table)

    def populate_sample_inventory(self):
        sample_inventory = [
            ['001', 'Говядина', 'Мясо', 'кг', '15.5', '5.0', 'Мясной двор'],
            ['002', 'Куриное филе', 'Мясо', 'кг', '8.2', '3.0', 'Птицефабрика'],
        ]
        self.inventory_table.setRowCount(len(sample_inventory))
        for row, item in enumerate(sample_inventory):
            for col, data in enumerate(item):
                self.inventory_table.setItem(row, col, QTableWidgetItem(str(data)))