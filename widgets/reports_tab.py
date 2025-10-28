from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QLabel, QComboBox, QDateEdit)
from PyQt5.QtCore import QDate

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

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