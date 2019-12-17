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
            if l[0] != pos.nom:
                pos = Momentos(l[0], x, float(l[len(l)-1]))
                #print(x, y)
            else:
                pos.momentoshu(x, float(l[len(l)-1]))
                #print(x, y)

            frames.append(pos)
        pos.printmomentos()
        return frames
    return None

def setNombre(y):
    if y == 0.:
        return "Parado"
    elif y == 1.:
        return "Sentadilla"
    elif y == 2.:
        return "Flyes"
    elif y == 3.:
        return "Abdominales"
    elif y == 4.:
        return "Lagartijas"
    else:
        return "No encontrado"

def main():
    # Create a VideoCapture object
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("videos/Angel Stand.mp4")
    n = 0
    y = []
    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Unable to read camera feed")

    file_o = open("basedatos.txt", "r")
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

            if cont < 10:
                frames.append(np.array(pos.hu).flatten())
                ys.append(pos.y)
                cont+=1
                #pos_hu = Momentos(pos.nombre, pos.hu, y)

            else:
                for i in range(len(frames_hu)):
                    if frames_hu[i]:
                        print(frames_hu[i].nom)
                        #print("for trainning: ", n)
                        w = nnt.trainning(frames_hu[i], frames, ys)
                        if y:
                            pop = y.pop()
                            if len(pop) == len(w):
                                y.append(pop)
                            else:
                                y.append(w)
                        else:
                            y.append(w)

                #pos.setName(texto)
                pos.setName(setNombre(y))
                cont = 0
                frames = []
                ys = []


            #'q' para detener el video
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            #fin del while
        else:
            break

        #termina el video


    file_c = open("entrenamiento.txt", "a+")
    guardar_archivo(file_c, y)

    file_o.close()
    file_c.close()
    cap.release()

    #cierra la ventana
    cv2.destroyAllWindows()
    print(n)


if __name__ == "__main__":
    main()
