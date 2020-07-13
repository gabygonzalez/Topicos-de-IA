import pygame
import os
import time
import math
from Nodos import Nodo

global car, car_x, car_y, rotacion, grafo
rotacion = 180
map = pygame.transform.scale(pygame.image.load(os.path.join("img", "costa_de_oro.jpg")), (540, 640))
car = pygame.transform.scale(pygame.image.load(os.path.join("img", "auto1.png")), (20, 10))
car = pygame.transform.rotate(car, rotacion)
pantalla = (0,0,540,640)
car_x = 390
car_y = 330
bandera = 0
b_next = 0
b_move = 0
move_x = 0
move_y = 0
car_next = []


def redraw_window(mapa, path):
    global win, map, b_next, b_move, move_x, move_y, car_next, car_x, car_y, car, rotacion, grafo
    win.blit(map, (0, 0))
    win.blit(car, (car_x, car_y))
    if grafo == 1:
        mapa.draw(win)
    if len(path) > 0:
        tam = len(path)
        for i in range(tam - 1):
            pygame.draw.line(win, (255, 0, 0), (path[i].x, path[i].y), (path[i + 1].x, path[i + 1].y), 2)

        if bandera > 0:
            if b_next == 0:
                car_next.append(path[tam - 1])
                b_next = 1
            if len(car_next) > 0:

                if (car_next[0].x == car_x + 8 and car_next[0].y == car_y + 4):
                    #print("entre")
                    b_next = 0
                    path.pop()
                    car_next.pop()
                    b_move = 0
                else:
                    car_x = car_next[0].x - 8
                    car_y = car_next[0].y - 4
                    rotacion += math.degrees(math.atan2(car_y, car_x))
                    #if math.degrees(math.atan2(car_y, car_x)) > rotacion:
                    #    rotacion -= math.degrees(math.atan2(car_y, car_x))
                    #else:
                    #    rotacion += math.degrees(math.atan2(car_y, car_x))
                    #print("rotacion: ", rotacion)
                    car = pygame.transform.scale(pygame.image.load(os.path.join("img", "auto1.png")), (20, 10))
                    car = pygame.transform.rotate(car, rotacion)
                    #print("car x: ", car_x, " - y: ", car_y)
                    #print("Pop: x: ", car_next[0].x, " - y: ", car_next[0].x)
                    # if b_move ==0:
                    #    move_x = (car_x - car_next[0].x) / 3
                    #    move_y = (car_y - car_next[0].y) / 3
                    #    b_move=1;
                    # else:
                    #    car_x -= move_x
                    #    car_y -= move_y
                    #
                    time.sleep(.5)

        #    u = path.pop()
        #    mover(u.x, u.y)
        #    draw += 1
        #    if draw == tam:
        #        draw = 0

    # map.draw(win)
    # pygame.draw.rect(win,(250,0,0),(0,0,540,640),5)
    pygame.display.update()

def leer_archivo(archivo_nodos, archivo_rels):
    if archivo_nodos:
        line = archivo_nodos.readline()
        #print(line)
        l = line.split()
        mapa = Nodo(int(l[0]), int(l[1]), l[2])
        for linea in archivo_nodos.readlines():
           #print(linea)
            v = linea.split()
            nuevo = Nodo(int(v[0]), int(v[1]), v[2])
            mapa.crear_nodos(nuevo)
            #print("")
            #mapa.imprimir()
        if archivo_rels:
            for linea in archivo_rels.readlines():
                v = linea.split()
                orig = mapa.buscar_clic(int(v[0]), int(v[1]))
                dest = mapa.buscar_clic(int(v[2]), int(v[3]))
                mapa.unir(orig, dest)
            archivo_rels.close()
        archivo_nodos.close()
        return mapa
    else:
        print("No se pudo abrir el archivo")
        return None

def guardar_archivo_nodos(mapa):
    file = open("nodos.txt", "a+")
    if file:
        mapa.guardar_nodos(file)
        file.close()

def guardar_archivo_rels(mapa):
    file = open("rels.txt", "a+")
    if file:
        mapa.guardar_rels(file)
        file.close()

def mover(x, y):
    move_x = (car_x - x) / 3
    move_y = (car_y - y) / 3
    for i in range(3):
        car_x -= move_x
        car_y -= move_y
        #win.blit(car, (car_x, car_y))
# mandar ventana?

def main():
    global bandera, grafo
    archivo_n = open("nodos.txt", "r")
    archivo_r = open("rels.txt", "r")
    if archivo_n and archivo_r:
        mapa = leer_archivo(archivo_n, archivo_r)  #checar que todos los nodos tengas minimo una relacion
    else:
        mapa = Nodo(398,334,'p')
    print("")
    print("")
    print("")
    #xy=34,20
    #mapa.imprimir()
    run = True
    camino = []
    grafo = 0
    while run:
        redraw_window(mapa, camino)
        #mapa.imprimir()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove("rels.txt")
                os.remove("nodos.txt")
                guardar_archivo_nodos(mapa)
                guardar_archivo_rels(mapa)
                run = False
                quit()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x, y)


            if event.type == pygame.MOUSEBUTTONUP:
                a, b = pygame.mouse.get_pos()
                print(a, b)

            if event.type == pygame.KEYDOWN:
                butt = pygame.key.get_pressed()
                for i in range(len(butt)):
                    if butt[i] == 1:
                        break
                if i == 110:
                    nuevo = Nodo(x, y, chr(112))
                    mapa.crear_nodos(nuevo)
                    mapa.imprimir()
                if i == 117:
                    orig = mapa.buscar_clic(x, y)
                    dest = mapa.buscar_clic(a, b)
                    if orig and dest:
                        mapa.unir(orig, dest)
                    else:
                        if orig is None:
                            print("no hay origen")
                        if dest is None:
                            print("no hay destino")
                if i == 98:
                    buscado = mapa.buscar_clic(x, y)
                    if buscado:
                        print("buscado: ", buscado.x, buscado.y)
                        buscado.aristas.imprimir_a()
                    else:
                        print("no se encontró el nodo")
                #if i == 116:
                    #temporal = Nodo(x, y, chr(i))
                    #mapa.crear_nodos(temporal)
                    #mapa.between(x, y)
                if i == 103:
                    if grafo == 1:
                        grafo = 0
                    else:
                        grafo = 1
                if i == 97:
                    destino = mapa.buscar_clic(x, y)
                    origen = mapa.buscar_clic(car_x+5, car_y+5)
                    if origen and destino:
                        mapa.set_heuristica(destino)
                        origen.dist = 0
                        visit = []
                        possible = []
                        origen.a_estrella(destino, possible, visit, 0)
                        #print("fin")
                        #for i in range(len(visit)):
                        #    print("padre: ", visit[i].padre.x, visit[i].padre.y)
                        #    print("hijo: ", visit[i].x, visit[i].y)
                        #    print(i, "\n")
                        last = visit.pop()
                        camino = []
                        last.get_camino(camino)
                        bandera = 1
                        #mostrar_camino(camino)
                        mapa.clear_all()

                    elif origen:
                        print("no existe destino")
                    else:
                        print("no existe origen")



    print("")
    print("")
    print("")
    mapa.imprimir()

width= 540
height = 640
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Rapidos y Furiosos Maps")
main()