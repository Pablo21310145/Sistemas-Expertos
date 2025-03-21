# -*- coding: utf-8 -*-
"""
Created on Mon Mar 03 22:22:12 2025

@author: Aspire
"""

def interfaz_usuario():
    es_dia = input("¿Es de día? (si/no): ").lower() == 'si'
    tiene_luna = input("¿Tiene luna? (si/no): ").lower() == 'si'

    hechos = {"es_dia": es_dia, "tiene_luna": tiene_luna}

    return hechos

# Recibir entrada del usuario
hechos_usuario = interfaz_usuario()
print(f"Hechos del usuario: {hechos_usuario}")

