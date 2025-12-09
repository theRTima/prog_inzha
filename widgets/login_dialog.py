from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Авторизация')
        self.setModal(True)
        self.resize(300, 200)
        
        layout = QVBoxLayout(self)
        
        # Поле логина
        layout.addWidget(QLabel('Логин:'))
        self.login_edit = QLineEdit()
        self.login_edit.setPlaceholderText('Введите логин')
        layout.addWidget(self.login_edit)
        
        # Поле пароля
        layout.addWidget(QLabel('Пароль:'))
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText('Введите пароль')
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)
        
        # Выбор роли
        layout.addWidget(QLabel('Роль:'))
        self.role_combo = QComboBox()
        self.role_combo.addItems([
            'Владелец',
            'Официант', 
            'Складовщик',
            'Бухгалтерия'
        ])
        layout.addWidget(self.role_combo)
        
        # Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Простая база пользователей (для демонстрации)
        self.users = {
            'admin': {'password': 'admin123', 'role': 'Владелец'},
            'waiter': {'password': 'waiter123', 'role': 'Официант'},
            'store': {'password': 'store123', 'role': 'Складовщик'},
            'account': {'password': 'account123', 'role': 'Бухгалтерия'}
        }

    def validate_and_accept(self):
        login = self.login_edit.text().strip()
        password = self.password_edit.text().strip()
        selected_role = self.role_combo.currentText()
        
        if not login or not password:
            QMessageBox.warning(self, 'Ошибка', 'Введите логин и пароль')
            return
        
        # Проверка пользователя
        if login in self.users:
            user = self.users[login]
            if user['password'] == password and user['role'] == selected_role:
                self.user_role = selected_role
                self.accept()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный пароль или роль')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пользователь не найден')

    def get_role(self):
        return getattr(self, 'user_role', None)