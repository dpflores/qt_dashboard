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


        # Delete after testing
        self.goto_dashboard()


        if user in USERS and password == PASSWORDS[user]:
            print('Hello {}'.format(user))
            self.goto_dashboard()
        else:
            
            self.error_label.setText('Invalid user or password')
    
    ## LOOOOK
    def goto_dashboard(self):
        dashboard_window = DashboardWindow()
        w.addWidget(dashboard_window)
        w.setCurrentIndex(w.currentIndex()+1)
        w.resize(1000, 550)
        # w.setFixedWidth(1000)
        # w.setFixedHeight(550)

        

class DashboardWindow(QDialog):
    def __init__(self):
        # SuperClass
        super(DashboardWindow,self).__init__()

        # Loading the UI
        loadUi("dashboard.ui", self)
        self.add_button.clicked.connect(self.add_button_fn)

        # Variables
        self.rows_count = 0
        self.cols_count = 0

        # Managing the layout (QGridLayout)
        self.ips = {}
    
    def add_button_fn(self):
        self.w2 = AddObjecWindow()
        self.w2.show() 
        self.w2.add_object_button.clicked.connect(self.add_object_button_fn)
        

    def add_object_button_fn(self):
        self.ips[self.w2.object_name.text()] = self.w2.ip.text()

        new_widget = GridObject(self.w2.object_name.text(),self.w2.ip.text())

        self.dashboard_layout.addWidget(new_widget, self.rows_count, self.cols_count)
        self.rows_count +=1
        self.w2.hide()




class AddObjecWindow(QDialog):
    def __init__(self):
        # SuperClass
        super(AddObjecWindow,self).__init__()
        # Loading the UI
        loadUi("new_object.ui", self)




class GridObject(QPushButton):
    def __init__(self,name, ip):
        super(GridObject, self).__init__()
        self.setStyleSheet('QPushButton { color: rgb(238, 238, 236);}')
        self.setText(name)
        self.ip = ip
        self.clicked.connect(self.go_link_fn)
    
    def go_link_fn(self):
        webbrowser.open(self.ip)















# def main():
app = QApplication(sys.argv)

# My windows 
login_window = LoginWindow()

# Widget configuration

w = QStackedWidget()
w.resize(480, 550)
# w.setFixedWidth(480)
# w.setFixedHeight(550)

# Adding windows
w.addWidget(login_window)


w.show() 
sys.exit(app.exec())

if __name__ == '__main__':
   main()