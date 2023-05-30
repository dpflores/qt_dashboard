
import cv2
import numpy as np
 

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt,QObject


from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as img

# Lectura de datos




img = cv2.imread('data/images/test_image.jpg')
TEST_IMG = img


# cv2.imshow('a',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

class ImageAnalyzer():

    def __init__(self):
        self.img = TEST_IMG
        self.img_analyzed = TEST_IMG
        self.display_height = 300
        self.display_width = 300


        self.qt_img = self.convert_to_qt(self.img)
        
    
    def convert_to_qt(self, cv_img):

        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def detect_objects(self):
        medidas = open("myFile.txt")
        linea = (medidas.readline()).split(';')
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