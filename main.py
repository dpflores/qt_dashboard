import sys
import webbrowser
import socket
import json
import csv
import time


from detector import *

# Core non-GUI classes used by other modules
from PyQt5.QtCore import *
# Graphical user interface components
from PyQt5.QtGui import *
#Classes for creating classic desktop-style UIs
from PyQt5.QtWidgets import *
# From QT designer to pyqt
from PyQt5.uic import *

USERS = ['dpflores','root']

PASSWORDS = {
    'dpflores':'delpiero2001',
    'root':'root'
}

VPN_ADRESS = '192.168.88.190'

JSON_FOLDER = 'data/.json/'
JSON_DASHBOARD_PATH = JSON_FOLDER + 'db_dashboard.json'




# TEST
LIST_1 = [1, 2, 3, 4]
LIST_2 = [2,3,4,5]


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

class ImageUpdaterThread(QThread):
    image_updated = pyqtSignal(QPixmap)

    def run(self):
        img_analyzer = ImageAnalyzer()
        while True:
            img_analyzer.update_image()
            qt_img = img_analyzer.qt_img
            self.image_updated.emit(qt_img)
            time.sleep(0.1)  # Ajusta el intervalo de actualización según tus necesidades

        

class DashboardWindow(QWidget):
    def __init__(self):
        super(DashboardWindow, self).__init__()

        self.img_analyzer = ImageAnalyzer()
        loadUi("qt_files/dashboard_widget2.ui", self)

        self.image_updater_thread = ImageUpdaterThread()
        self.image_updater_thread.image_updated.connect(self.update_image)
        self.image_updater_thread.start()

        self.export_button.clicked.connect(self.export_fn)
        self.analyze_button.clicked.connect(self.analyze_fn)

        # Establece la imagen inicial
        qt_img = self.img_analyzer.qt_img
        self.image_label.setPixmap(qt_img)

        
    def analyze_fn(self):
        # Acá colocar code de analisis
        data = self.img_analyzer.get_data()
        print(data)
        longitud, n_peces = self.img_analyzer.detect_objects(data)
        print(n_peces)
        self.fill_table(longitud, n_peces)

    def update_image(self, qt_img):
        self.image_label.setPixmap(qt_img.scaledToWidth(self.image_label.width()))

    
    def export_fn(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Guardar Archivo', QDir.homePath()+"/data.csv", "CSV Files(*.csv *.txt)")
        if filename:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Escribir los encabezados en el archivo CSV
                headers = []
                for column in range(self.table_sum.columnCount()):
                    header_item = self.table_sum.horizontalHeaderItem(column)
                    if header_item is not None:
                        headers.append(header_item.text())
                    else:
                        headers.append('')
                writer.writerow(headers)

                # Escribir los datos en el archivo CSV
                for row in range(self.table_sum.rowCount()):
                    row_data = []
                    for column in range(self.table_sum.columnCount()):
                        item = self.table_sum.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)

    def fill_table(self, lista1, lista2):
        num_filas = max(len(lista1), len(lista2))
        self.table_sum.setRowCount(num_filas)
        self.table_sum.setColumnCount(2)

        for fila in range(num_filas):
            if fila < len(lista1):
                valor1 = lista1[fila]
                item1 = QTableWidgetItem(str(valor1))
                item1.setTextAlignment(Qt.AlignCenter)  # Centra el texto en la celda
                self.table_sum.setItem(fila, 0, item1)

            if fila < len(lista2):
                valor2 = lista2[fila]
                item2 = QTableWidgetItem(str(valor2))
                item2.setTextAlignment(Qt.AlignCenter)  # Centra el texto en la celda
                self.table_sum.setItem(fila, 1, item2)


def main():

    
    app = QApplication(sys.argv)

    # My windows 
    

    # Widget configuration

    # Adding windows

    w = LoginWindow()


    # w.resize(700, 550)

    w.show() 
    sys.exit(app.exec())

if __name__ == '__main__':
   main()