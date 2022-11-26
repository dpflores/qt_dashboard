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

USERS = ['del', 'diego','hugo','root']

PASSWORDS = {
    'del':'123',
    'diego':'321',
    'hugo':'123',
    'root':'axotec'
}

VPN_ADRESS = '192.168.88.190'

JSON_FOLDER = 'data/.json/'
JSON_DASHBOARD_PATH = JSON_FOLDER + 'db_dashboard.json'

# Images
DEFAULT_IMAGE='data/images/axotec.jpg'

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
        
        
        # self.dw.resize(1000, 550)
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

        # Index
        self.current_index = 0

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
            self.load_data()
        except:
            pass
    
    def check_index(self):
        # 5 columnas por fila
        
       
        self.current_index +=1
        if self.current_index%(5) == 0 and self.current_index != 0:
            self.rows_count +=1
            self.cols_count = 0
        else:
            self.cols_count += 1
        

        
    def load_data(self):
        with open(JSON_DASHBOARD_PATH, "r") as read_file:
                self.db_data = json.load(read_file)

        for key in self.db_data:
            
            new_widget = GridObject(key,self.db_data[key][0],self.db_data[key][1],self.db_data[key][2], self)
            self.dashboard_layout.itemAt(0).widget().hide()
            self.dashboard_layout.addWidget(new_widget, self.rows_count, self.cols_count)
            
            self.check_index()

            
    def add_button_fn(self):
        self.w2 = AddObjecWindow()
        self.w2.show() 
        self.w2.add_object_button.clicked.connect(self.add_object_button_fn)
        

    def add_object_button_fn(self):
        # self.ips[self.w2.object_name.text()] = self.w2.ip.text()
        if self.current_index<10:
            new_widget = GridObject(self.current_index, self.w2.object_name.text(),self.w2.ip.text(), DEFAULT_IMAGE,self)
            self.dashboard_layout.itemAt(0).widget().hide()
            self.dashboard_layout.addWidget(new_widget, self.rows_count, self.cols_count)
            

            # 5 columnas por fila
            self.check_index()
        else:
            pass ###
        print(self.current_index, self.rows_count, self.cols_count)
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
    def __init__(self,index, name, ip, image_path, dashboard_window):
        super(GridObject, self).__init__()


        self.dashboard_window = dashboard_window
        
        # Size
        # self.setGeometry(10,10,10,10)
        self.index = index
        self.name = name
        self.ip = ip
        self.image_path = image_path

        # Saving data
        self.dashboard_window.db_data[index] = [name, ip, image_path]

        self.layout = QHBoxLayout()

        # Editando el dashboard object
        self.dashboard_object = DashboardObject()

        do = self.dashboard_object

        # Buttons functions
        do.link_button.clicked.connect(self.go_link_fn)
        do.edit_button.clicked.connect(self.go_edit_fn)
        do.delete_button.clicked.connect(self.go_delete_fn)
        
        # Buttons style
        do.edit_button.setIcon(QIcon('icons/edit.svg'))
        do.delete_button.setIcon(QIcon('icons/delete.svg'))

        # Name, image and data
        do.name_label.setText(self.name)
        do.link_button.setIcon(QIcon(self.image_path))
        do.link_button.setIconSize(QSize(150,150))


        self.layout.addWidget(self.dashboard_object)
        
        
        self.setLayout(self.layout)
    
    def go_link_fn(self):
        link = "http://"+self.ip+":1880/ui"
        webbrowser.get().open(link)

    def go_edit_fn(self):
        self.w2 = EditObjecWindow()
        self.w2.show() 
        self.w2.object_name.setText(self.name)
        self.w2.ip.setText(self.ip)
        self.w2.edit_object_button.clicked.connect(self.edit_object_button_fn)
        self.w2.change_image_button.clicked.connect(self.change_image_button_fn)

        # Adding the image
        pixmap = QPixmap(self.image_path)
        pixmap = pixmap.scaledToWidth(150)
        self.w2.image_label.setPixmap(QPixmap(pixmap))
    
    def edit_object_button_fn(self):
        # self.grid_object.w_link = GridButtonLink(self.w2.object_name.text(), self.w2.ip)
        self.update_layout(self.w2.object_name.text(), self.w2.ip.text(),self.image_path)
        self.w2.deleteLater()
    
    def change_image_button_fn(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'c\\', 'Image files (*.jpg *.gif)')
        # print(fname)
        if fname[0]:
            self.image_path = fname[0]
    

        # Updating the image
        pixmap = QPixmap(self.image_path)
        pixmap = pixmap.scaledToWidth(150)
        self.w2.image_label.setPixmap(QPixmap(pixmap))

    def update_layout(self, name, ip, image_path):

        # Updating data
        self.name = name
        self.ip = ip
        self.image_path = image_path

        # New data
        self.dashboard_window.db_data[self.index] = [name, ip, image_path]

        self.dashboard_object.name_label.setText(self.name)
        self.dashboard_object.link_button.setIcon(QIcon(self.image_path))
        self.dashboard_object.link_button.setIconSize(QSize(150,150))

        self.setLayout(self.layout)

    def go_delete_fn(self):
        # Removing the previous data
        try:
            self.dashboard_window.db_data.pop(self.index)
        except:
            pass

        
        
        if self.dashboard_window.current_index%5 == 0 and self.dashboard_window.current_index != 0:
            self.dashboard_window.rows_count -=1
            self.dashboard_window.cols_count = 4
        else:
            self.dashboard_window.cols_count -= 1

        self.dashboard_window.current_index -= 1
        if self.dashboard_window.current_index == 0:
            self.dashboard_window.dashboard_layout.itemAt(0).widget().show()
        
        print(self.dashboard_window.current_index, self.dashboard_window.rows_count, self.dashboard_window.cols_count)

        self.deleteLater()
        

class DashboardObject(QWidget):
    def __init__(self):
        # SuperClass
        super(DashboardObject,self).__init__()
        # Loading the UI
        loadUi("qt_files/dashboard_object.ui", self)



def main():
    app = QApplication(sys.argv)

    # My windows 
    

    # Widget configuration

    # Adding windows

    w = LoginWindow()

    w.show() 
    sys.exit(app.exec())

if __name__ == '__main__':
   main()