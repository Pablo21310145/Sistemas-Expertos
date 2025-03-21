# Base de conocimiento con reglas
base_de_conocimiento = {
    "si_es_dia": "Es necesario encender las luces",
    "si_tiene_luna": "Es probable que haya más visibilidad nocturna"
}

def consultar_base_conocimiento(hechos):
    for hecho, conclusion in base_de_conocimiento.items():
        if hechos.get(hecho):
            print(conclusion)

hechos = {"si_es_dia": True, "si_tiene_luna": False}
consultar_base_conocimiento(hechos)
