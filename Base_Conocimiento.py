# -*- coding: utf-8 -*-
"""
Created on Mon Mar 03 22:10:45 2025

@author: Aspire
"""

# Definición de hechos
hechos = {
    "es_dia": True,
    "tiene_luna": False,
}

# Definición de reglas
def es_noche(hechos):
    if not hechos["es_dia"] and hechos["tiene_luna"]:
        return True
    return False

# Inferencia
if es_noche(hechos):
    print("Es de noche")
else:
    print("Es de día")

