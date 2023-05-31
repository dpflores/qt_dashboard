
import cv2
import numpy as np
 

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt,QObject

try:
    from o2x5xx import ImageClient
except ModuleNotFoundError:
    from o2x5xx.device.image_client import ImageClient
    
try:
    from o2x5xx import O2x5xxDevice
except ModuleNotFoundError:
    from o2x5xx.device.client import O2x5xxDevice

from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as img

from datetime import datetime


# Lectura de datos

img = cv2.imread('data/images/test_image.jpg')
TEST_IMG = img


# cv2.imshow('a',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

class ImageAnalyzer():

    def __init__(self,address='192.168.0.5', port=50010, img_height=300, img_width=300):
        
        # El device es para obtener la salida de data de la cámara y el imageclient es para la foto
        self.device = O2x5xxDevice(address, port)
        self.image_client = ImageClient(address, port)


        self.img = self.get_frame()

        self.img_analyzed = self.get_frame()

        self.display_height = img_height
        self.display_width = img_width

        self.qt_img = self.convert_to_qt(self.img)

    def get_data(self):
        ticket, answer = self.device.read_next_answer()

        if ticket == b"0000":
            # Add a line index and a timestamp at the start of the line
            answer = "DATA" + ";" + answer.decode() + ";" + str(datetime.now())
            return answer

    def get_frame(self):
        self.image_client.read_next_frames()
        return self.image_client.frames[-1]
    
    def update_image(self):
        self.img = self.get_frame()
        self.qt_img = self.convert_to_qt(self.img)

    def convert_to_qt(self, cv_img):

        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def detect_objects(self, data_string):
        medidas = open("myFile.txt")
        linea = (medidas.readline()).split(';')

        # medidas = data_string
        # linea = medidas.split(';')
        # Datos de la muestra
        # Muestra 0
        muestra = int(linea[0])

        # MODELO
        # Validacion del modelo
        validacion_modelo = bool(linea[2])

        # ID del ROI
        id_ROI = int(linea[3])

        # Validacion del ROI
        validacion_ROI = bool(linea[4])

        # Numero de objeto
        n_objetos = int(linea[5])

        # Superficie total
        superficie_total = float(linea[6])

        # Datos de los objetos
        id_objeto = []    # 7
        posx = []         # 9
        posy = []         # 10
        ancho = []        # 11
        altura = []       # 12
        th = []           # 21

        for i in range(n_objetos):
            id_objeto.append(float(linea[7+19*i]))
            posx.append(float(linea[9+19*i]))
            posy.append(float(linea[10+19*i]))
            ancho.append(float(linea[11+19*i]))
            altura.append(float(linea[12+19*i]))
            th.append(float(linea[21+19*i]))

        # Transformación de ancho y altura
        for i in range(n_objetos):
            ancho[i] = ancho[i]*68.2/1280
            altura[i] = altura[i]*51.1/960

        # Lista de peces y longitud
        longitud = [x/10 for x in range(100, 160, 5)]  # desde 10 hasta 15.5
        n_peces = [x*0 for x in range(100, 160, 5)]

        for j in range(len(longitud)):
            for i in range(n_objetos):
                if 9.75 + j*0.5 < ancho[i] < 10.5 + j*0.5:
                    n_peces[j] = n_peces[j] + 1

        
        return longitud, n_peces