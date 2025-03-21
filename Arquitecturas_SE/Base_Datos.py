
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 03 22:40:05 2025

@author: Aspire
"""
# Base de datos simple con información sobre productos
productos = {
    'producto_1': {'nombre': 'Monitor', 'precio': 250},
    'producto_2': {'nombre': 'Teclado', 'precio': 50},
}

def obtener_producto_info(codigo_producto):
    return productos.get(codigo_producto, "Producto no encontrado")

print(obtener_producto_info('producto_1'))

