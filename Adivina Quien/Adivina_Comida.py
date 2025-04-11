import json

class Nodo:
    def __init__(self, pregunta=None, comida=None):
        self.pregunta = pregunta  # Si es nodo interno
        self.comida = comida      # Si es nodo hoja (respuesta)
        self.si = None            # Rama para "sí"
        self.no = None            # Rama para "no"

def nodo_a_dict(nodo):
    if nodo.comida:
        return {"comida": nodo.comida}
    else:
        return {
            "pregunta": nodo.pregunta,
            "si": nodo_a_dict(nodo.si),
            "no": nodo_a_dict(nodo.no)
        }

def dict_a_nodo(data):
    if "comida" in data:
        return Nodo(comida=data["comida"])
    else:
        nodo = Nodo(pregunta=data["pregunta"])
        nodo.si = dict_a_nodo(data["si"])
        nodo.no = dict_a_nodo(data["no"])
        return nodo

def guardar_arbol(raiz, archivo="arbol_comidas.json"):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(nodo_a_dict(raiz), f, ensure_ascii=False, indent=4)

def cargar_arbol(archivo="arbol_comidas.json"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
            return dict_a_nodo(data)
    except FileNotFoundError:
        return crear_arbol_inicial()
    
def crear_arbol_inicial():
    raiz = Nodo("¿Es dulce?")

    dulce = Nodo("¿Se come al desayuno?")
    no_dulce = Nodo("¿Tiene carne?")

    dulce.si = Nodo(comida="Hotcakes")
    dulce.no = Nodo(comida="Pastel")

    no_dulce.si = Nodo("¿Es mexicana?")
    no_dulce.no = Nodo(comida="Ensalada")

    no_dulce.si.si = Nodo(comida="Tacos")
    no_dulce.si.no = Nodo(comida="Hamburguesa")

    raiz.si = dulce
    raiz.no = no_dulce

    return raiz

def preguntar_si_no(pregunta):
    while True:
        respuesta = input(pregunta + " (s/n): ").lower()
        if respuesta in ["s", "n"]:
            return respuesta == "s"
        print("Por favor responde con 's' para sí o 'n' para no.")

def jugar(raiz):
    actual = raiz
    padre = None
    ultima_rama = None  # "si" o "no"

    while actual.comida is None:
        respuesta = preguntar_si_no(actual.pregunta)
        padre = actual
        ultima_rama = "si" if respuesta else "no"
        actual = actual.si if respuesta else actual.no

    # Llegamos a una hoja
    acertado = preguntar_si_no(f"¿Estás pensando en {actual.comida}?")

    if acertado:
        print("¡Genial! Adiviné correctamente 😄")
    else:
        nueva_comida = input("Oh no... ¿En qué comida estabas pensando?: ")
        nueva_pregunta = input(f"Escribe una pregunta que distinga a {nueva_comida} de {actual.comida}: ")
        respuesta_para_nueva = preguntar_si_no(f"Para {nueva_comida}, ¿la respuesta sería sí?")

        nuevo_nodo = Nodo(pregunta=nueva_pregunta)
        if respuesta_para_nueva:
            nuevo_nodo.si = Nodo(comida=nueva_comida)
            nuevo_nodo.no = actual
        else:
            nuevo_nodo.no = Nodo(comida=nueva_comida)
            nuevo_nodo.si = actual

        if padre:
            if ultima_rama == "si":
                padre.si = nuevo_nodo
            else:
                padre.no = nuevo_nodo
        else:
            # Si no había padre, estamos en la raíz
            raiz.pregunta = nuevo_nodo.pregunta
            raiz.si = nuevo_nodo.si
            raiz.no = nuevo_nodo.no
            raiz.comida = None

        print("¡Gracias! Aprendí una nueva comida.")

def main():
    print("\t\t🍲 Bienvenido al juego: Adivina la comida\n\nPiensa en una comida y yo intentare adivinarla")
    print("\n¿Listo? ¡Adelante!\n\nLa comida en la que estas pensando: ")
    raiz = cargar_arbol()

    while True:
        jugar(raiz)
        if not preguntar_si_no("¿Quieres jugar otra vez?"):
            break

    guardar_arbol(raiz)
    print("Gracias por jugar ¡Hasta la próxima! 😋")


if __name__ == "__main__":
    main()
