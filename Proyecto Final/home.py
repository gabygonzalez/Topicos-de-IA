import cv2
import numpy as np
from postura import Postura
from postura import Momentos
import nn_trainer as nnt


def guardar_archivo(file, frames, y):
    if file and frames:
        pos = frames.pop()
        file.write(str(pos.nombre) + " " + str(pos.hu[0][0]) + " " + str(pos.hu[1][0]) + " " + str(pos.hu[2][0]) + " " + str(pos.hu[3][0]) + " " + str(pos.hu[4][0]) + " " + str(pos.hu[5][0]) + " " + str(pos.hu[6][0]) + " " + str(y) + '\n')
        guardar_archivo(file, frames, y)

def leer_archivo(file):
    if file:
        frames = []
        x =[]
        line = file.readline()
        l = line.split()
        for i in range(1, 8):
            x.append(float(l[i]))
        pos = Momentos(l[0], x, l[9])
        frames.append(pos)
        n = 1
        for linea in file.readlines():
            l = linea.split()
            x = list(map(lambda x: float(x), l[1:8]))
            #print(x)
            if l[0] != pos.nom:
                pos = Momentos(l[0], x, l[9])
                #print(x, y)
            else:
                pos.momentoshu(x, l[9])
                #print(x, y)

            frames.append(pos)
        pos.printmomentos()
        return frames
    return None

def main():
    # Create a VideoCapture object
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("videos/Ale Lagartijas.mp4")
    n = 0

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Unable to read camera feed")


    frames = []
    frames_hu = []
    y = []

    while (True):
        ret, frame = cap.read()
        n+=1
        if ret == True:

            # Display the resulting frame
            #cv2.imshow('frame', frame)

            # Read display in gs
            im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            bg = cv2.imread("images/fondo.jpg", cv2.IMREAD_GRAYSCALE)

            blurred_im = cv2.GaussianBlur(im, (5, 5), 1)
            blurred_bg = cv2.GaussianBlur(bg, (5, 5), 1)

            bim = cv2.bilateralFilter(im, 9, 75, 75)
            bbg = cv2.bilateralFilter(bg, 9, 75, 75)

            #dif = cv2.absdiff(bg, im)
            dif = cv2.absdiff(bbg, blurred_im)
            pos = Postura(dif, frame)
            print(len(frames_hu))
            for i in range(len(frames_hu)):
                if frames_hu[i]:
                    #print(frames_hu[i].hu, frames_hu[i].y)
                    print("for trainning: ", n)
                    #texto = nnt.trainning(frames_hu[i], pos)  #  for en el que cambie de parado->sentadilla->etc

            y = 4.

            #pos.setName(texto)
            pos.setName("Lagartijas")
            pos_hu = Momentos(pos.nombre, pos.hu, y)

            frames.append(pos)
            frames_hu.append(pos_hu)


            #'q' para detener el video
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            #fin del while
        else:
            break

        #termina el video


    file_c = open("database.txt", "a+")
    guardar_archivo(file_c, frames, y)

    #file_o.close()
    file_c.close()
    cap.release()

    #cierra la ventana
    cv2.destroyAllWindows()
    print(n)


if __name__ == "__main__":
    main()
