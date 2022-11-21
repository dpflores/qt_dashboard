import sys
import webbrowser
import socket
import json



# Core non-GUI classes used by other modules
from PyQt5.QtCore import *
# Graphical user interface components
from PyQt5.QtGui import *
#Classes for creating classic desktop-style UIs
from PyQt5.QtWidgets import *
# From QT designer to pyqt
from PyQt5.uic import *

USERS = ['del', 'diego','hugo']

PASSWORDS = {
    'del':'123',
    'diego':'321',
    'hugo':'123'
}

VPN_ADRESS = '192.168.88.190'

JSON_FOLDER = 'data/.json/'
JSON_DASHBOARD_PATH = JSON_FOLDER + 'db_dashboard.json'


class LoginWindow(QWidget): 
    def __init__(self):
        # SuperClass
        super(LoginWindow,self).__init__()

        # Loading the UI
        loadUi("qt_files/login_widget.ui", self)


        self.sign_button.clicked.connect(self.sign_fn)

        # To hide the password
        self.password.setEchoMode(QLineEdit.Password)




    def sign_fn(self):
        user = self.user.text()
        password = self.password.text()


        # Delete after testing
        self.goto_dashboard()


        if user in USERS and password == PASSWORDS[user]:
            # print('Hello {}'.format(user))
            self.goto_dashboard()
        else:
            
            self.error_label.setText('Invalid user or password')
    

    def goto_dashboard(self):
        self.hide()
        self.dw = DashboardWindow()
        
        
        self.dw.resize(1000, 550)
        self.dw.show()
        # w.setFixedWidth(1000)
        # w.setFixedHeight(550)
    
    # def reject(self): 
    #     # to avoid the esc key closing 
    #     pass

        

class DashboardWindow(QWidget):
    def __init__(self):
        # SuperClass
        super(DashboardWindow,self).__init__()

        

        # with open('dashboard.db','wb') as f:
        #     pickle.dump(dashboard,f)

        # Loading the UI
        loadUi("qt_files/dashboard_widget.ui", self)
        self.add_button.clicked.connect(self.add_button_fn)

        # Variables
        self.rows_count = 0
        self.cols_count = 0

        # Managing the layout (QGridLayout)
        self.db_data = {}

        # 
        try:
            connection = socket.gethostbyaddr(VPN_ADRESS)
            self.connected = True

            self.indicator.setText('connected')
            self.indicator.setStyleSheet("background-color:rgb(138, 226, 52)")
            
        except socket.herror:
            self.connected = False
            self.indicator.setText('disconnected')
            self.indicator.setStyleSheet("background-color:rgb(239, 41, 41)")
        
        # Recover the previous configuration
        try:
            with open(JSON_DASHBOARD_PATH, "r") as read_file:
                self.db_data = json.load(read_file)

            for key in self.db_data:
                new_widget = GridObject(key,self.db_data[key],self)
                self.dashboard_layout.itemAt(0).widget().hide()
                self.dashboard_layout.addWidget(new_widget, self.rows_count, self.cols_count)
                self.rows_count +=1
        except:
            pass

    

    def add_button_fn(self):
        self.w2 = AddObjecWindow()
        self.w2.show() 
        self.w2.add_object_button.clicked.connect(self.add_object_button_fn)
        

    def add_object_button_fn(self):
        # self.ips[self.w2.object_name.text()] = self.w2.ip.text()

        new_widget = GridObject(self.w2.object_name.text(),self.w2.ip.text(),self)
        self.dashboard_layout.itemAt(0).widget().hide()
        self.dashboard_layout.addWidget(new_widget, self.rows_count, self.cols_count)
        self.rows_count +=1
        self.w2.deleteLater()

    def closeEvent(self, event):
        # Defaul close event
        # print(self.db_data)

        with open(JSON_DASHBOARD_PATH, "w") as f:
            json.dump(self.db_data, f)
    

    
class AddObjecWindow(QDialog):
    def __init__(self):
        # SuperClass
        super(AddObjecWindow,self).__init__()
        # Loading the UI
        loadUi("qt_files/new_object.ui", self)

class EditObjecWindow(QDialog):
    def __init__(self):
        # SuperClass
        super(EditObjecWindow,self).__init__()
        # Loading the UI
        loadUi("qt_files/edit_object.ui", self)



class GridObject(QFrame):
    def __init__(self,name, ip, dashboard_window):
        super(GridObject, self).__init__()

        self.dashboard_window = dashboard_window
        
        self.name = name
        self.ip = ip

        # Saving data
        self.dashboard_window.db_data[name] = ip

        self.w_link = GridButtonLink(self.name,self.ip)
        self.w_edit = GridButtonEdit(self)
        self.w_delete = GridButtonDelete(self)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.addWidget(self.w_link,stretch=10)
        self.layout.addWidget(self.w_edit,stretch=1)
        self.layout.addWidget(self.w_delete,stretch=1)
        self.setLayout(self.layout)

    def update_layout(self,name, ip):
        self.w_link.deleteLater()
        self.w_edit.deleteLater()
        self.w_delete.deleteLater()

        # Removing the previous data
        self.dashboard_window.db_data.pop(self.name)

        # Updating data
        self.name = name
        self.ip = ip

        # New data
        self.dashboard_window.db_data[name] = ip

        self.w_link = GridButtonLink(self.name,self.ip)
        self.w_edit = GridButtonEdit(self)
        self.w_delete = GridButtonDelete(self)

        self.layout.addWidget(self.w_link,stretch=10)
        self.layout.addWidget(self.w_edit,stretch=1)
        self.layout.addWidget(self.w_delete,stretch=1)

        self.setLayout(self.layout)
    
    def delete(self):
        # Removing the previous data
        self.dashboard_window.db_data.pop(self.name)

        self.deleteLater()
        self.dashboard_window.rows_count -=1
        if self.dashboard_window.rows_count == 0:
            self.dashboard_window.dashboard_layout.itemAt(0).widget().show()


class GridButtonLink(QPushButton):
    def __init__(self,name, ip):
        super(GridButtonLink, self).__init__()
      
        self.setStyleSheet('QPushButton { color: rgb(0, 0, 0);background-color: rgb(235, 235, 235);}'
                            "QPushButton::hover"
                             "{"
                             "background-color : rgb(170, 170, 170);"
                             "}")
        self.setText(name)
        self.ip = ip
        self.clicked.connect(self.go_link_fn)
    
    def go_link_fn(self):
        link = "http://"+self.ip+":1880/ui"
        webbrowser.get().open(link)

class GridButtonEdit(QPushButton):
    def __init__(self,grid_object):
        super(GridButtonEdit, self).__init__()
        self.setStyleSheet('QPushButton { color: rgb(0, 0, 0);background-color: rgb(235, 235, 235);}'
                            "QPushButton::hover"
                             "{"
                             "background-color : rgb(170, 170, 170);"
                             "}")
        self.setIcon(QIcon('icons/edit.svg'))
        self.clicked.connect(self.go_edit_fn)

        self.grid_object = grid_object
    
    def go_edit_fn(self):
        self.w2 = EditObjecWindow()
        self.w2.show() 
        self.w2.object_name.setText(self.grid_object.name)
        self.w2.ip.setText(self.grid_object.ip)
        self.w2.edit_object_button.clicked.connect(self.edit_object_button_fn)
    
    def edit_object_button_fn(self):
        # self.grid_object.w_link = GridButtonLink(self.w2.object_name.text(), self.w2.ip)
        self.grid_object.update_layout(self.w2.object_name.text(), self.w2.ip.text())

class GridButtonDelete(QPushButton):
    def __init__(self,grid_object):
        super(GridButtonDelete, self).__init__()
        self.setStyleSheet('QPushButton { color: rgb(0, 0, 0);background-color: rgb(235, 235, 235);}'
                            "QPushButton::hover"
                             "{"
                             "background-color : rgb(170, 170, 170);"
                             "}")
        self.setIcon(QIcon('icons/delete.svg'))
        self.clicked.connect(self.go_delete_fn)
        
        self.grid_object = grid_object

    def go_delete_fn(self):
        self.grid_object.delete()


def main():
    app = QApplication(sys.argv)

    # My windows 
    

    # Widget configuration

    # Adding windows

    w = LoginWindow()

    w.resize(700, 550)

    w.show() 
    sys.exit(app.exec())

if __name__ == '__main__':
   main()