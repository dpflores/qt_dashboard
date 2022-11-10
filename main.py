import sys
import webbrowser


# Core non-GUI classes used by other modules
from PyQt5.QtCore import *
# Graphical user interface components
from PyQt5.QtGui import *
#Classes for creating classic desktop-style UIs
from PyQt5.QtWidgets import *
# From QT designer to pyqt
from PyQt5.uic import *

USERS = ['del', 'diego']

PASSWORDS = {
    'del':'123',
    'diego':'321'
}

class LoginWindow(QDialog): 
    def __init__(self):
        # SuperClass
        super(LoginWindow,self).__init__()

        # Loading the UI
        loadUi("login.ui", self)
        self.sign_button.clicked.connect(self.sign_fn)

        # To hide the password
        self.password.setEchoMode(QLineEdit.Password)

    def sign_fn(self):
        user = self.user.text()
        password = self.password.text()

        # Delete after test
        self.goto_dashboard()
        
        if user in USERS and password == PASSWORDS[user]:
            print('Hello {}'.format(user))
            self.goto_dashboard()
    
    def goto_dashboard(self):
        dashboard_window = DashboardWindow()

        

class DashboardWindow(QDialog):
    def __init__(self):
        # SuperClass
        super(LoginWindow,self).__init__()

        # Loading the UI
        loadUi("dashboard.ui", self)
        self.go_link1.clicked.connect(self.go_link1_fn)

        # To hide the password
        self.password.setEchoMode(QLineEdit.Password)
    
    def go_link1_fn():
        webbrowser.open('google.com')










def main():
    app = QApplication(sys.argv)

    # My windows 
    login_window = LoginWindow()

    # Widget configuration
    w = QStackedWidget()
    w.setFixedWidth(480)
    w.setFixedHeight(550)

    # Adding windows
    w.addWidget(login_window)


    w.show() 
    sys.exit(app.exec())

if __name__ == '__main__':
   main()