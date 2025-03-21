
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 03 22:28:51 2025

@author: Aspire
"""

def explicar(hechos, reglas, conclusiones):
    explicacion = []
    for conclusion in conclusiones:
        for regla in reglas:
            if regla["conclusion"] == conclusion:
                explicacion.append(f"Para llegar a '{conclusion}', se usó la regla con condiciones: {regla['condiciones']}")
    return explicacion

# Explicar la conclusión
explicacion = explicar(hechos, reglas, nuevas_conclusiones)
for paso in explicacion:
    print(paso)

