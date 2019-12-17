import cv2
import numpy as np

class Postura():

    def __init__(self, img, orig):
        self.img = img
        self.orginal = orig
        self.hu = self.momentosHU(img)
        self.nombre = ""
        self.y = float(np.random.randint(0, 4))

    def area(self, img):
        mayor = cv2.__version__.split('.')[0]
        if mayor == '3':  #encuentra los contornos
            _, contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        else:
            contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        areas = []
        for c in contours:
            areas.append(cv2.contourArea(c))  #calcula el área de los contornos

        #ordena el arreglo de áreas por tamaño
        sorted_areas = sorted(zip(areas, contours), key=lambda x: x[0], reverse=True)

        x, y, w, h = cv2.boundingRect(sorted_areas[1][1])

        if w < 190 and h < 590:  #compara para saber si regresar el primer área más grande o el segundo
            return sorted_areas[0][1]
        else:
            return sorted_areas[1][1]

    def momentosHU(self, img):  #imagen ya en grayscale
        _,im = cv2.threshold(img, 32, 255, cv2.THRESH_BINARY_INV)
        contours = self.area(im)

        cv2.drawContours(self.orginal, contours, -1, (0, 255, 0), 2)

        cv2.imshow("Mask", im)  #binarizado
        cv2.imshow("Frame", self.orginal)  #contornos
        moment = cv2.moments(contours) #calcula momentos
        huMoments = cv2.HuMoments(moment) #calcula momentos de hu
        #print(huMoments)
        #self.hu = huMoments
        return huMoments

    def setName(self, nombre):
        self.nombre = nombre



####################################################


class Momentos():

    def __init__(self, nom, hu, y):
        self.nom = nom
        self.hu = [hu]
        self.y = [y]

    def momentoshu(self, hu, y):
        self.hu.append(hu)
        self.y.append(y)

    def printmomentos(self):
       # print(np.array(self.y))
        arr = np.array(self.hu) #list(map(lambda x:np.array(x),self.hu)))
        #print(np.array(self.hu).flatten())
        print(arr)