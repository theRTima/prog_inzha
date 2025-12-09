import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from widgets.login_dialog import LoginDialog

def main():
    app = QApplication(sys.argv)
    
    # Показываем диалог авторизации
    login_dialog = LoginDialog()
    if login_dialog.exec_() == LoginDialog.Accepted:
        role = login_dialog.get_role()
        if role:
            window = MainWindow(role=role)
            window.show()
            sys.exit(app.exec_())
        else:
            print("Роль не определена")
    else:
        print("Авторизация отменена")

if __name__ == "__main__":
    main()