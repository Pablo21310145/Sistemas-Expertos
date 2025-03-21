# -*- coding: utf-8 -*-
"""
Created on Mon Mar 03 22:15:45 2025

@author: Aspire
"""

def forward_chaining(hechos, reglas):
    nuevas_conclusiones = []
    for regla in reglas:
        if regla["condiciones"].issubset(hechos):
            nuevas_conclusiones.append(regla["conclusion"])
    return nuevas_conclusiones

# Hechos iniciales
hechos = {"tiene_luna": False, "es_dia": True}

# Reglas
reglas = [
    {"condiciones": {"tiene_luna", "es_dia"}, "conclusion": "es_de_noche"},
    {"condiciones": {"es_dia"}, "conclusion": "es_de_dia"},
]

# Aplicar Forward Chaining
nuevas_conclusiones = forward_chaining(hechos, reglas)
print(nuevas_conclusiones)

