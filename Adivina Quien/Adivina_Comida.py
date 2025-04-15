import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from pathlib import Path

class Nodo:
    def __init__(self, pregunta=None, comida=None):
        self.pregunta = pregunta
        self.comida = comida
        self.si = None
        self.no = None

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
    if Path(archivo).exists():
        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
            return dict_a_nodo(data)
    else:
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

class JuegoComida:
    def __init__(self, ventana, raiz_arbol):
        self.ventana = ventana
        self.raiz = raiz_arbol
        self.actual = raiz_arbol

        self.saludo = tk.Label(ventana, text="🍲 Bienvenido al juego: Adivina la comida\n\nPiensa en una comida y yo intentaré adivinarla\n\n¿Listo? ¡Adelante!", font=("Arial", 12), justify="center")
        self.saludo.pack(pady=20)

        self.boton_comenzar = tk.Button(ventana, text="¡Comenzar!", width=20, command=self.iniciar_juego)
        self.boton_comenzar.pack(pady=10)

        self.etiqueta_pregunta = tk.Label(ventana, text="", font=("Arial", 14))
        self.etiqueta_pregunta.pack(pady=20)
        self.etiqueta_pregunta.pack_forget()

        self.boton_si = tk.Button(ventana, text="Sí", width=20, command=self.responder_si)
        self.boton_si.pack(pady=20)
        self.boton_si.pack_forget()

        self.boton_no = tk.Button(ventana, text="No", width=20, command=self.responder_no)
        self.boton_no.pack(pady=20)
        self.boton_no.pack_forget()

        self.boton_reiniciar = tk.Button(ventana, text="Reiniciar Juego", width=20, command=self.reiniciar_juego)
        self.boton_reiniciar.pack(pady=20)
        self.boton_reiniciar.pack_forget()

        ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def iniciar_juego(self):
        self.saludo.pack_forget()
        self.boton_comenzar.pack_forget()
        self.etiqueta_pregunta.config(text=self.actual.pregunta)
        self.etiqueta_pregunta.pack()
        self.boton_si.pack()
        self.boton_no.pack()

    def responder_si(self):
        self._responder(True)

    def responder_no(self):
        self._responder(False)

    def _responder(self, respuesta):
        if self.actual.comida is None:
            self.actual = self.actual.si if respuesta else self.actual.no

            if self.actual.comida is None:
                self.etiqueta_pregunta.config(text=self.actual.pregunta)
            else:
                self.adivinacion()
        else:
            self.adivinacion()

    def adivinacion(self):
        self.etiqueta_pregunta.config(text=f"¿Estás pensando en {self.actual.comida}?")
        self.boton_si.config(command=self.confirmar_si)
        self.boton_no.config(command=self.confirmar_no)

    def confirmar_si(self):
        messagebox.showinfo("¡Adiviné!", f"¡Genial! Estaba pensando en {self.actual.comida} 😄")
        self.etiqueta_pregunta.config(text="Gracias por jugar ¡Hasta la próxima! 😋")
        self._finalizar_partida()

    def confirmar_no(self):
        nueva_comida = simpledialog.askstring("Nueva Comida", "¿En qué comida estabas pensando?")
        nueva_pregunta = simpledialog.askstring("Nueva Pregunta", f"Escribe una pregunta que distinga a {nueva_comida} de {self.actual.comida}: ")
        respuesta_para_nueva = messagebox.askyesno("Nueva Pregunta", f"Para {nueva_comida}, ¿la respuesta sería sí?")

        nuevo_nodo = Nodo(pregunta=nueva_pregunta)
        if respuesta_para_nueva:
            nuevo_nodo.si = Nodo(comida=nueva_comida)
            nuevo_nodo.no = self.actual
        else:
            nuevo_nodo.no = Nodo(comida=nueva_comida)
            nuevo_nodo.si = self.actual

        # Reemplazar nodo actual por el nuevo
        self.actual.pregunta = nuevo_nodo.pregunta
        self.actual.comida = None
        self.actual.si = nuevo_nodo.si
        self.actual.no = nuevo_nodo.no

        messagebox.showinfo("¡Gracias!", "¡Aprendí una nueva comida! 😋")
        self.etiqueta_pregunta.config(text="Gracias por jugar ¡Hasta la próxima! 😋")
        self._finalizar_partida()

    def _finalizar_partida(self):
        self.boton_si.pack_forget()
        self.boton_no.pack_forget()
        self.boton_reiniciar.pack()

    def reiniciar_juego(self):
        guardar_arbol(self.raiz)
        self.actual = self.raiz
        self.boton_reiniciar.pack_forget()
        self.etiqueta_pregunta.config(text=self.actual.pregunta)
        self.boton_si.config(command=self.responder_si)
        self.boton_no.config(command=self.responder_no)
        self.boton_si.pack()
        self.boton_no.pack()

    def cerrar_ventana(self):
        guardar_arbol(self.raiz)
        messagebox.showinfo("¡Gracias!", "Gracias por jugar ¡Hasta la próxima! 😋")
        self.ventana.destroy()


# Ejecutar la aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Adivina la Comida")
    ventana.geometry("450x400")
    ventana.resizable(False, False)

    raiz_arbol = cargar_arbol()
    juego = JuegoComida(ventana, raiz_arbol)

    ventana.mainloop()
