import pygame
import os
from Aristas import Arista

class Nodo(object):

	def __init__(self, x, y, tipo):
		self.x = x
		self.y = y
		self.tipo = tipo
		self.nodos = None
		self.aristas = None
		self.heuristica = None
		self.dist = None
		self.padre = None

	def draw(self, win):
		if self is None:
			return None
		xy = self.x, self.y
		pygame.draw.circle(win, (255, 0, 0), xy, 2)
		if self.aristas:
			self.aristas.draw(self.x, self.y, win)
		if self.nodos:
			self.nodos.draw(win)

	def insertar(self, valor, nuevo):
		if self.aristas is None:
			a = Arista(valor, nuevo)
			self.aristas = a
		else:
			a = Arista(valor, nuevo)
			self.aristas.insertar_a(a)

	def buscar(self, x, y):
		if self is None:
			return None
		if self.x == x and self.y == y:
			return self
		if self.nodos:
			return self.nodos.buscar(x, y)

	def crear_nodos(self, nuevo):
		if self is None:
			self = nuevo
			return
		n = self.buscar(nuevo.x, nuevo.y)
		if n is None:
			if self.nodos is None:
				self.nodos = nuevo
			else:
				self.nodos.crear_nodos(nuevo)
		else:
			#n.nodos = nuevo
			return

	def buscar_clic(self, x, y):
		if self is None:
			return None
		if self.x < x+5 and self.x > x-5 and self.y < y+5 and self.y > y-5:
			return self
		if self.nodos:
			return self.nodos.buscar_clic(x, y)

	def buscar_between(self, x, y, lista_nodos):
		if self is None:
			print("aquí llega")
			return lista_nodos
		if self.x < x+40 and self.x > x-40 and self.y < y+40 and self.y > y-40:
			#xy = (self.x, self.y)
			lista_nodos.append(self)
		if self.nodos:
			lista_nodos = self.nodos.buscar_between(x, y, lista_nodos)
		return lista_nodos


	def imprimir(self):
		if self is None:
			return None
		print("x: ", self.x, "  y: ", self.y)
		if self.aristas:
			self.aristas.imprimir_a()
		if self.nodos:
			self.nodos.imprimir()

	def unir(self, origen, destino):
		if self is None:
			return
		print("origen: ", origen.x, origen.y, "  destino: ", destino.x, destino.y)
		valor = (origen.x - destino.x)  + (origen.y - destino.y)
		origen.insertar(valor, destino)
		#origen.imprimir()
		#print("se unió: ", origen.x, origen.y, "  con: ", destino.x, destino.y)

	def guardar_nodos(self, archivo):
		if self is None:
			return None
		if self.tipo == 'p':
			archivo.write(str(self.x) +" "+ str(self.y) +" "+ self.tipo + '\n')
		if self.nodos:
			self.nodos.guardar_nodos(archivo)

	def guardar_rels(self, archivo):
		if self is None:
			return
		if self.aristas and self.tipo == 'p':
			self.aristas.guardar_aristas(archivo, self)
		if self.nodos:
			self.nodos.guardar_rels(archivo)

	def between(self, x, y):
		if self is None:
			return
		lista_nodos = []
		lista_nodos = self.buscar_between(x, y, lista_nodos)
		print("final: ", lista_nodos)
		lista_aristas = []
		for x in range(len(lista_nodos)):
			lista_aristas = lista_nodos[x].aristas.buscar_in_a(lista_nodos, lista_aristas)
		print(lista_aristas)

	def set_heuristica(self, destino):
		if self is None:
			return
		hx = destino.x - self.x
		hy = destino.y - self.y
		if (hx + hy) < 0:
			self.heuristica = -(hx + hy)
		else:
			self.heuristica = hx + hy
		if self.nodos:
			self.nodos.set_heuristica(destino)

	def a_estrella(self, destino, nodos_posibles, visitados, i):
		if self is None:
			return visitados

		if self == destino:
			visitados.append(self)
			return visitados

		if self.aristas:
			return self.aristas.a_estrella_aristas(self, destino, nodos_posibles, visitados, i)

	def lista_nodos(self, lista, visitados):
		if self is None:
			return
		if self.aristas:
			self.aristas.lista_aristas(lista, visitados, self)

	def get_camino(self, camino):
		if self is None or self.padre is None:
			camino.append(self)
			return
		camino.append(self)
		if self.padre:
			self.padre.get_camino(camino)

	def clear_all(self):
		if self is None:
			return
		self.heuristica = None
		self.dist = None
		self.padre = None
		if self.nodos:
			self.nodos.clear_all()