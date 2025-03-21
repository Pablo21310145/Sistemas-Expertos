
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 03 22:38:55 2025

@author: Aspire
"""
# Simulamos un sensor de temperatura
import random

def obtener_temperatura():
    return random.uniform(20.0, 30.0)  # Temperatura aleatoria entre 20 y 30 grados

temperatura = obtener_temperatura()
print(f"Temperatura actual: {temperatura:.2f}°C")

