# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 21:26:12 2025

@author: Aspire
"""
'''
Codigo de busqueda bidireccional que ayuda a encontrar el camino mas corto entre dos ciudades
simultaneamente tanto desde el inicio como del final
'''

from collections import deque  # Importa deque, una cola de doble extremo, para manejar la expansión de nodos.

class Grafo:
    def __init__(self):
        self.grafo = {}  # Inicializa un diccionario vacío para representar el grafo.

    def agregar_arista(self, ciudad1, ciudad2):
        # Si la ciudad1 no está en el grafo, se agrega una lista vacía.
        if ciudad1 not in self.grafo:
            self.grafo[ciudad1] = []
        # Si la ciudad2 no está en el grafo, se agrega una lista vacía.
        if ciudad2 not in self.grafo:
            self.grafo[ciudad2] = []
        # Agrega ciudad2 a la lista de vecinos de ciudad1 (arista bidireccional).
        self.grafo[ciudad1].append(ciudad2)
        # Agrega ciudad1 a la lista de vecinos de ciudad2 (arista bidireccional).
        self.grafo[ciudad2].append(ciudad1)

    def busqueda_bidireccional(self, inicio, meta):
        # Si el inicio y la meta son la misma ciudad, retorna un camino con esa ciudad.
        if inicio == meta:
            return [inicio]

        # Diccionarios para marcar las ciudades visitadas desde el inicio y desde la meta.
        visitados_inicio = {inicio: None}  # Almacena las ciudades visitadas desde el inicio.
        visitados_meta = {meta: None}  # Almacena las ciudades visitadas desde la meta.

        # Colas para manejar las ciudades a explorar desde el inicio y la meta.
        cola_inicio = deque([inicio])  # Cola de expansión desde el inicio.
        cola_meta = deque([meta])  # Cola de expansión desde la meta.

        # Bucle que continúa mientras ambas colas tengan ciudades por explorar.
        while cola_inicio and cola_meta:
            # Expande el nodo desde la dirección del inicio.
            camino = self._expandir_nodo(cola_inicio, visitados_inicio, visitados_meta)
            if camino:  # Si se encuentra un camino, lo retorna.
                return camino

            # Expande el nodo desde la dirección de la meta.
            camino = self._expandir_nodo(cola_meta, visitados_meta, visitados_inicio)
            if camino:  # Si se encuentra un camino, lo retorna.
                return camino

        # Si no se encuentra un camino, retorna None.
        return None

    def _expandir_nodo(self, cola, visitados_primarios, visitados_secundarios):
        # Extrae la ciudad actual de la cola.
        actual = cola.popleft()
        
        # Recorre los vecinos de la ciudad actual.
        for vecino in self.grafo.get(actual, []):
            # Si el vecino no ha sido visitado en la dirección actual.
            if vecino not in visitados_primarios:
                # Marca el vecino como visitado, indicando de dónde vino (la ciudad actual).
                visitados_primarios[vecino] = actual
                # Añade el vecino a la cola para explorarlo en la siguiente iteración.
                cola.append(vecino)

                # Si el vecino también ha sido visitado desde la otra dirección, se ha encontrado un camino.
                if vecino in visitados_secundarios:
                    # Construye y retorna el camino completo uniendo ambos lados.
                    return self._construir_camino(visitados_primarios, visitados_secundarios, vecino)
        return None  # Si no se encuentra intersección, retorna None.

    def _construir_camino(self, visitados_inicio, visitados_meta, interseccion):
        # Construye el camino desde el inicio hasta la intersección.
        camino_desde_inicio = []
        actual = interseccion
        # Recorre hacia atrás, siguiendo las marcas de visitado, hasta llegar al inicio.
        while actual:
            camino_desde_inicio.append(actual)
            actual = visitados_inicio[actual]
        # Invierte el camino para que quede en el orden correcto.
        camino_desde_inicio = camino_desde_inicio[::-1]

        # Construye el camino desde la meta hasta la intersección.
        camino_desde_meta = []
        actual = visitados_meta[interseccion]
        # Recorre hacia atrás, siguiendo las marcas de visitado, hasta llegar a la meta.
        while actual:
            camino_desde_meta.append(actual)
            actual = visitados_meta[actual]

        # Une el camino desde el inicio con el camino desde la meta para formar el camino completo.
        return camino_desde_inicio + camino_desde_meta


# Definir el grafo (ciudades y conexiones)
grafo = Grafo()  # Crea una instancia del grafo.
# Agregar conexiones entre ciudades (aristas).
grafo.agregar_arista("Ciudad de México", "Puebla")
grafo.agregar_arista("Puebla", "Monterrey")
grafo.agregar_arista("Monterrey", "Cancún")
grafo.agregar_arista("Ciudad de México", "Toluca")
grafo.agregar_arista("Toluca", "Monterrey")
grafo.agregar_arista("Toluca", "Cancún")

# Lista de ciudades disponibles para elegir
ciudades = ["Ciudad de México", "Cancún", "Puebla", "Monterrey", "Toluca"]

# Mostrar las ciudades disponibles
print("Ciudades disponibles:")
for i, ciudad in enumerate(ciudades, 1):
    print(f"{i}. {ciudad}")

# Pedir al usuario que elija la ciudad de origen
origen_idx = int(input("Selecciona la ciudad de origen (1-5): ")) - 1
origen = ciudades[origen_idx]

# Pedir al usuario que elija la ciudad de destino
destino_idx = int(input("Selecciona la ciudad de destino (1-5): ")) - 1
destino = ciudades[destino_idx]

# Ejecutar la búsqueda bidireccional entre las ciudades elegidas
camino = grafo.busqueda_bidireccional(origen, destino)
if camino:
    # Si se encuentra un camino, se imprime.
    print("Camino encontrado:", " -> ".join(camino))
else:
    # Si no se encuentra un camino, se imprime un mensaje de error.
    print("No se encontró un camino.")
