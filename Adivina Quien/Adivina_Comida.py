
import tkinter as tk
import json
import os
import shutil

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

def guardar_arbol(raiz, archivo="arbol_comidas.json", backup="arbol_comidas_backup.json"):
    if os.path.exists(archivo):
        shutil.copy(archivo, backup)  # Crear respaldo antes de sobreescribir
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(nodo_a_dict(raiz), f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("⚠️ Error al guardar el árbol:", e)
        if os.path.exists(backup):
            shutil.copy(backup, archivo)
            print("🔁 Restaurado desde respaldo.")

def cargar_arbol(archivo="arbol_comidas.json", backup="arbol_comidas_backup.json"):
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                return dict_a_nodo(data)
        except Exception as e:
            print("⚠️ Error al cargar el archivo principal:", e)

    if os.path.exists(backup):
        try:
            print("🛠️ Cargando respaldo...")
            with open(backup, "r", encoding="utf-8") as f:
                data = json.load(f)
                return dict_a_nodo(data)
        except Exception as e:
            print("🚫 También falló el respaldo:", e)

    print("📦 No se encontró archivo válido. Se usará árbol inicial.")
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

        self.ventana.configure(bg="#f3e5f5")  # Lila muy suave

        self.saludo = tk.Label(ventana, text="🍲 Bienvenido al juego: Adivina la comida\n\nPiensa en una comida y yo intentaré adivinarla\n\n¿Listo? ¡Adelante!", font=("Segoe UI", 13, "bold"), justify="center", bg="#f3e5f5", fg="#4a148c")
        self.saludo.pack(pady=20)

        # Botón de inicio
        self.boton_comenzar = tk.Button(ventana, text="¡Comenzar!", width=20, font=("Segoe UI", 11), bg="#ffcc70", fg="black", command=self.iniciar_juego)
        self._agregar_hover(self.boton_comenzar, "#ffcc70", "#ffe09f")
        self.boton_comenzar.pack(pady=10)

        self.etiqueta_pregunta = tk.Label(ventana, text="", font=("Segoe UI", 14), bg="#f3e5f5", fg="#333")
        self.etiqueta_pregunta.pack(pady=20)
        self.etiqueta_pregunta.pack_forget()

        # Botón de si
        self.boton_si = tk.Button(ventana, text="Sí", width=15, font=("Segoe UI", 11), bg="#a5d6a7", command=self.responder_si)
        self._agregar_hover(self.boton_si, "#a5d6a7", "#81c784")
        self.boton_si.pack(pady=10)
        self.boton_si.pack_forget()

        # Botón de no
        self.boton_no = tk.Button(ventana, text="No", width=15, font=("Segoe UI", 11), bg="#ffccbc", command=self.responder_no)
        self._agregar_hover(self.boton_no, "#ffccbc", "#ffab91")
        self.boton_no.pack(pady=10)
        self.boton_no.pack_forget()

        # Campos de entrada para comida y pregunta
        self.entrada_comida = tk.Entry(ventana, font=("Segoe UI", 11), width=35)
        self.entrada_pregunta = tk.Entry(ventana, font=("Segoe UI", 11), width=45)

        # Botón de confirmación para guardar la comida y la pregunta
        self.boton_confirmar_nueva = tk.Button(ventana, text="Guardar", font=("Segoe UI", 11), bg="#d0bfff", command=self._pasar_a_etapa_pregunta)
        self._agregar_hover(self.boton_confirmar_nueva, "#d0bfff", "#e6d6ff")

        # Botón de reiniciar juego
        self.boton_reiniciar = tk.Button(ventana, text="Reiniciar Juego", width=20, font=("Segoe UI", 11), bg="#87cefa", command=self.reiniciar_juego)
        self._agregar_hover(self.boton_reiniciar, "#87cefa", "#b0e0ff")
        self.boton_reiniciar.pack(pady=10)
        self.boton_reiniciar.pack_forget()

        # Botón de salir
        self.boton_salir = tk.Button(ventana, text="Salir", width=20, font=("Segoe UI", 11), bg="#f08080", command=self.salir_juego)
        self._agregar_hover(self.boton_salir, "#f08080", "#fa9e9e")
        self.boton_salir.pack(pady=5)
        self.boton_salir.pack_forget()

        ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def _agregar_hover(self, boton, color_normal, color_hover):
        boton.bind("<Enter>", lambda e: boton.config(bg=color_hover))
        boton.bind("<Leave>", lambda e: boton.config(bg=color_normal))

    def iniciar_juego(self):
        self.saludo.pack_forget()
        self.boton_comenzar.pack_forget()
        self.etiqueta_pregunta.config(text=self.actual.pregunta)
        self.etiqueta_pregunta.pack()
        self.boton_si.config(command=self.responder_si)
        self.boton_no.config(command=self.responder_no)
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
                self.etiqueta_pregunta.config(text="Espera, estoy pensando... 🤔")  # Mensaje de "pensando..."
                self.boton_si.pack_forget()
                self.boton_no.pack_forget()
                self.ventana.after(1500, self.adivinacion)# Pausar por 2 segundos (2000 milisegundos)
                #self.adivinacion()
        else:
            self.etiqueta_pregunta.config(text="Espera, estoy pensando... 🤔")
            self.boton_si.pack_forget()
            self.boton_no.pack_forget()
            self.ventana.after(1500, self.adivinacion)
            #self.adivinacion()


    def adivinacion(self):
        self.etiqueta_pregunta.config(text=f"¿Estás pensando en {self.actual.comida}?")
        self.boton_si.pack()
        self.boton_no.pack()
        self.boton_si.config(command=self.confirmar_si)
        self.boton_no.config(command=self.confirmar_no)

    def confirmar_si(self):
        self.etiqueta_pregunta.config(text=f"¡Genial! Estaba pensando en {self.actual.comida} 😄")
        self._finalizar_partida()

    def confirmar_no(self):
        self.boton_si.pack_forget()
        self.boton_no.pack_forget()

        self.etiqueta_pregunta.config(text="Oh no... ¿En qué comida estabas pensando?")
        
        self.etiqueta_comida = tk.Label(self.ventana, text="Ingresa el nombre de la comida:", font=("Segoe UI", 11), bg="#f3e5f5")
        self.etiqueta_comida.pack()
        
        self.entrada_comida.delete(0, tk.END)
        self.entrada_comida.pack(pady=5)

        self.boton_confirmar_nueva.config(text="Siguiente", command=self._pasar_a_etapa_pregunta)
        self.boton_confirmar_nueva.pack(pady=10)

    def _pasar_a_etapa_pregunta(self):
        comida = self.entrada_comida.get().strip()
        if not comida:
            self.etiqueta_pregunta.config(text="⚠️ Por favor escribe un nombre válido para la comida.")
            return

        self.nueva_comida_temp = comida
        self.entrada_comida.pack_forget()
        self.etiqueta_comida.pack_forget()
        self.boton_confirmar_nueva.pack_forget()

        texto_pregunta = f"Escribe una pregunta que distinga a {self.nueva_comida_temp} de {self.actual.comida}:" 
        self.etiqueta_nueva_pregunta = tk.Label(self.ventana, text=texto_pregunta, font=("Segoe UI", 11), bg="#f3e5f5", wraplength=400, justify="left")
        self.etiqueta_nueva_pregunta.pack()

        self.entrada_pregunta.delete(0, tk.END)
        self.entrada_pregunta.pack(pady=5)

        self.boton_confirmar_nueva.config(text="Confirmar", command=self._pasar_a_etapa_confirmacion)
        self.boton_confirmar_nueva.pack(pady=10)

    def _pasar_a_etapa_confirmacion(self):
        pregunta = self.entrada_pregunta.get().strip()
        if not pregunta:
            self.etiqueta_pregunta.config(text="⚠️ Por favor escribe una pregunta válida.")
            return

        self.nueva_pregunta_temp = pregunta
        self.entrada_pregunta.pack_forget()
        self.etiqueta_nueva_pregunta.pack_forget()
        self.boton_confirmar_nueva.pack_forget()

        self.etiqueta_pregunta.config(text=f"Para {self.nueva_comida_temp}, ¿la respuesta sería 'sí'?")
        self.boton_si.config(command=lambda: self._crear_nodo_nuevo(True))
        self.boton_no.config(command=lambda: self._crear_nodo_nuevo(False))
        self.boton_si.pack()
        self.boton_no.pack()

    def _crear_nodo_nuevo(self, respuesta_si):
        nueva_comida = self.nueva_comida_temp
        nueva_pregunta = self.nueva_pregunta_temp
    
        # Se crea un nuevo nodo con la pregunta
        nuevo_nodo = Nodo(pregunta=nueva_pregunta)
    
        # Dependiendo de la respuesta, se asigna comida o el nodo actual al nuevo nodo
        if respuesta_si:
            nuevo_nodo.si = Nodo(comida=nueva_comida)
            nuevo_nodo.no = Nodo(comida=self.actual.comida)  # Nodo con la comida anterior
        else:
            nuevo_nodo.no = Nodo(comida=nueva_comida)
            nuevo_nodo.si = Nodo(comida=self.actual.comida)  # Nodo con la comida anterior
    
        # Actualiza el nodo actual con la nueva pregunta
        self.actual.pregunta = nueva_pregunta
        self.actual.comida = None
        self.actual.si = nuevo_nodo.si
        self.actual.no = nuevo_nodo.no
    
        self.etiqueta_pregunta.config(text="¡Gracias! He aprendido una nueva comida 😋")
        self._finalizar_partida()

    def _finalizar_partida(self):
        self.boton_si.pack_forget()
        self.boton_no.pack_forget()
        self.boton_reiniciar.pack()
        self.boton_salir.pack()

    def reiniciar_juego(self):
        guardar_arbol(self.raiz)
        self.actual = self.raiz
        self.boton_reiniciar.pack_forget()
        self.boton_salir.pack_forget()
        self.etiqueta_pregunta.config(text=self.actual.pregunta)
        self.boton_si.config(command=self.responder_si)
        self.boton_no.config(command=self.responder_no)
        self.boton_si.pack()
        self.boton_no.pack()

    def salir_juego(self):
        self.etiqueta_pregunta.config(text="Gracias por jugar.\nHasta la próxima 👋")
        self.boton_salir.pack_forget()
        self.boton_reiniciar.pack_forget()
        self.ventana.after(2000, self.cerrar_ventana)

    def cerrar_ventana(self):
        guardar_arbol(self.raiz)
        self.ventana.destroy()

# Ejecutar la aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Adivina la Comida")
    ventana.geometry("450x400")
    ventana.resizable(False, False)
    ventana.iconbitmap("pizza_food.ico")

    raiz_arbol = cargar_arbol()
    juego = JuegoComida(ventana, raiz_arbol)

    ventana.mainloop()
