import cv2
import numpy as np
from postura import Postura
from postura import Momentos
import nn_trainer as nnt


def guardar_archivo(file, y):
    if file and y:
        y1 = y.pop()
        file.write(str(y1[0]) + " " + str(y1[1]) + "\n")
        guardar_archivo(file, y)

def leer_archivo(file):
    if file:
        frames = []
        x =[]
        line = file.readline()
        l = line.split()
        for i in range(1, 8):
            x.append(float(l[i]))
        pos = Momentos(l[0], x, float(l[len(l)-1]))
        frames.append(pos)
        n = 1
        for linea in file.readlines():
            l = linea.split()
            x = list(map(lambda x: float(x), l[1:8]))
            #print(x)
            pos.momentoshu(x, float(l[len(l)-1]))
            #print(x, y)
        pos.printmomentos()
        return pos
    return None

def count(list):
    cero = 0
    uno = 0
    dos = 0
    tres = 0
    cuatro = 0
    n = len(list)

    for i in range(n):
        if 0. == list[i]:
            cero+=1
        elif 1. == list[i]:
            uno+=1
        elif 2. == list[i]:
            dos+=1
        elif 3. == list[i]:
            tres+=1
        else:
            cuatro+=1

    return (cero, uno, dos, tres, cuatro)

def sort(list):
    aux = [0,1]
    aux1 = []
    arr0 = []
    arr1 = []
    n = len(list)
    for i in range(n):
        aux1 = list.pop()
        arr0.append(aux1[0])
        arr1.append(aux1[1][0])

    print(arr0, arr1)

    for i in range(n):
        for j in range(n-1):
            if arr0[j] < arr0[j + 1]:
                aux[0] = arr0[j]
                aux[1] = arr1[j]
                arr0[j] = arr0[j + 1]
                arr1[j] = arr1[j + 1]
                arr0[j + 1] = aux[0]
                arr1[j + 1] = aux[1]

    print(arr0, arr1)
    x = count(arr1)
    return arr1[0], x

def setNombre(y):
    #ordenar arreglo por y[0], mayor == posicion
    y = sort(y)
    x = count(y[1])

    if y[0] == 0.: #or x[0] == 5:
        return "Parado"
    elif y[0] == 1.: # or x[0] == 3 and x[1] == 1 and x[2] == 2:
        return "Sentadilla"
    elif y[0] == 2.: # or x[0] == 4 and x[2] == 2:
        return "Flyes"
    elif y[0] == 3.: # or x[1] == 5 and x[2] == 1 or x[1] == 1 and x[2] == 2:
        return "Abdominales"
    elif y[0] == 4.: # or x[4] == 3:
        return "Lagartijas"
    else:
        return "No encontrado"

def main():
    # Create a VideoCapture object
    #cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture("videos/originales/angel.mp4")
    cap = cv2.VideoCapture("videos/angel sentadilla.mp4")
    n = 0
    y = []
    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Unable to read camera feed")

    file_o = open("database.txt", "r")
    if file_o:
        frames_hu = leer_archivo(file_o)

    frames = []
    ys = []
    cont = 0

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
            #print(len(frames_hu))

            if cont < 11:
                frames.append(np.array(pos.hu).flatten())
                ys.append(pos.y)
                cont+=1

            else:
                if frames_hu:
                    #print("for trainning: ", n)
                    y.append(nnt.trainning(frames_hu, frames, ys))

                cont = 0
                frames = []
                ys = []

                if y and len(y) > 5:
                    pos.setName(setNombre(y))
                    print(pos.nombre)
                    y = []

            #'q' para detener el video
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            #fin del while
        else:
            break

        #termina el video

    pos.setName(setNombre(y))
    print(pos.nombre)
    #file_c = open("basedatos.txt", "a+")
    #guardar_archivo(file_c, y)

    file_o.close()
    #file_c.close()
    cap.release()

    #cierra la ventana
    cv2.destroyAllWindows()
    print(n)


if __name__ == "__main__":
    main()
