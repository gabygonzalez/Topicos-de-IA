import pygame

class Arista(object):

    def __init__(self, valor, nodo):
        self.valor = valor
        self.nodo = nodo
        self.arista = None
        self.num_a = 1

    def draw(self, x_o, y_o,  win):
        if self is None:
            return None
        x = self.nodo.x
        y = self.nodo.y
        pygame.draw.line(win, (0,0,255), (x_o, y_o), (x, y), 1)
        if self.arista:
            self.arista.draw(x_o, y_o, win)

    def insertar_a(self, arista):
        if self.arista is None:
            self.arista = arista
            self.num_a += 1
            return
        elif self.arista == arista:
            return
        else:
            self.arista.insertar_a(arista)

    def imprimir_a(self):
        if self is None:
            return
        print("-->valor: ", self.valor, "   nodo_x: ", self.nodo.x, "  nodo_y: ", self.nodo.y)
        if self.arista:
            self.arista.imprimir_a()

    def buscar_a(self, x, y):
        if self is None:
            return None
        if self.nodo.x == x and self.nodo.y == y:
            return self
        if self.arista:
            return self.arista.buscar_a(x, y)

    def buscar_in_a(self, lista_nodos, lista):
        if self is None:
            return lista
        nodo_d = lista_nodos.pop()
        if self.arista.nodo == nodo_d:
            lista.append(self)
        if self.arista:
            lista = self.arista.buscar_in_a(lista_nodos, lista)
            lista_nodos.append(nodo_d)
        return lista

    def guardar_aristas(self, archivo, origen):
        if self is None:
            return
        archivo.write(str(origen.x) +" "+ str(origen.y) +" "+ str(self.nodo.x) +" "+ str(self.nodo.y) + '\n')
        if self.arista:
            self.arista.guardar_aristas(archivo, origen)

    def lista_aristas(self, lista, visitados, origen):
        if self is None:
            return lista
        if self.nodo not in visitados:
            if self.nodo.dist is not None:
                if origen.dist + self.valor < self.nodo.dist:
                    self.nodo.padre = origen
                    self.nodo.dist = origen.dist + self.valor
            else:
                self.nodo.padre = origen
                self.nodo.dist = origen.dist + self.valor

            f = origen.dist + self.valor + self.nodo.heuristica
            lista.append((self.nodo, f))
        if self.arista:
            self.arista.lista_aristas(lista, visitados, origen)

    def a_estrella_aristas(self, origen, destino, nodos_posibles, visitados, i):
        if self is None:
            return visitados
        self.lista_aristas(nodos_posibles, visitados, origen)
        #origen.lista_nodos(nodos_posibles, visitados)
        nodos_posibles.sort(key=lambda x: x[1])
        expandir = nodos_posibles.pop(0)
        visitados.append(expandir[0])
        expandir[0].a_estrella(destino, nodos_posibles, visitados, i+1)

