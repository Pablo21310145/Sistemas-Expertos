import random
import json
import pygame
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


import os
print(os.getcwd())
print(os.path.isfile("Tab.png"))  # ¿Existe?

"""
def guardar_historias_en_json(historias, nombre_archivo="historias.json"):
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(historias, f, ensure_ascii=False, indent=4)
        print(f"✅ Historias guardadas en {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error al guardar el archivo JSON: {e}")
"""


def cargar_historias_desde_json(nombre_archivo="historias.json"):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            historias = json.load(f)
        return historias
    except Exception as e:
        print(f"⚠️ Error al cargar el archivo JSON: {e}")
        return []
    
    
pygame.mixer.init()

pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.play(-1)  # El -1 hace que se repita infinitamente

class ClueJuego:
    def __init__(self):
        self.personajes = ["Tu hermana", "Tu mamá", "Tu papá", "Tu hermano", "Tu primo"]
        self.lugares = ["Estudio", "Cocina", "Biblioteca", "Billar", "Comedor"]
        self.armas = ["Candelabro", "Cuchillo de cocina", "Revólver", "Cuerda", "Llave inglesa"]
        self.historias = cargar_historias_desde_json() or self.historias_predeterminadas()
        self.historia_actual = random.choice(self.historias)
        self.pistas_restantes = 5
    
    
    
    def historias_predeterminadas(self):
        return [
            
            
        ]



    def obtener_pista(self, tipo, seleccion):
        if tipo == "personaje":
            personaje = seleccion
            pista = self.historia_actual["personajes"].get(personaje, "")
        elif tipo == "lugar":
            pista = self.historia_actual["lugares"].get(seleccion, "")
        elif tipo == "arma":
            pista = self.historia_actual["armas"].get(seleccion, "")
        return pista




def mostrar_pista():
    if juego.pistas_restantes > 0:
        tipo_pista = seleccion_tipo_pista.get()
        seleccion = seleccion_opcion.get()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una opción primero.")
            return
        pista = juego.obtener_pista(tipo_pista, seleccion)
        messagebox.showinfo("Pista", pista)
        juego.pistas_restantes -= 1
        etiqueta_pistas_restantes.config(text="Pistas restantes: {}".format(juego.pistas_restantes))
    else:
        boton_pista.grid_forget()
        mostrar_adivinanza()

def actualizar_lista(*args):
    categoria_seleccionada = seleccion_tipo_pista.get()
    if categoria_seleccionada == "personaje":
        lista_opciones["menu"].delete(0, "end")
        for personaje in juego.personajes:
            lista_opciones["menu"].add_command(label=personaje, command=tk._setit(seleccion_opcion, personaje))
    elif categoria_seleccionada == "lugar":
        lista_opciones["menu"].delete(0, "end")
        for lugar in juego.lugares:
            lista_opciones["menu"].add_command(label=lugar, command=tk._setit(seleccion_opcion, lugar))
    elif categoria_seleccionada == "arma":
        lista_opciones["menu"].delete(0, "end")
        for arma in juego.armas:
            lista_opciones["menu"].add_command(label=arma, command=tk._setit(seleccion_opcion, arma))

def mostrar_adivinanza():
    seleccion_opcion_culpable = tk.StringVar()
    seleccion_opcion_lugar = tk.StringVar()
    seleccion_opcion_arma = tk.StringVar()
    
    def comprobar_adivinanza():
        respuesta_culpable = seleccion_opcion_culpable.get()
        respuesta_lugar = seleccion_opcion_lugar.get()
        respuesta_arma = seleccion_opcion_arma.get()
        
        if (respuesta_culpable == juego.historia_actual["culpable"] and
            respuesta_lugar == juego.historia_actual["lugar"] and
            respuesta_arma == juego.historia_actual["arma"]):
            messagebox.showinfo("Resultado", "¡Felicidades! Has resuelto el misterio correctamente.", parent=ventana_adivinanza)
            
            # Preguntar si quiere volver a jugar
            respuesta = messagebox.askyesno("¿Jugar otra vez?", "¿Quieres jugar otra vez?", parent=ventana_adivinanza)
            if respuesta:
                ventana_adivinanza.destroy()
                reiniciar_juego()
            else:
                ventana.destroy()
                
        else:
            aciertos = []
            if respuesta_culpable == juego.historia_actual["culpable"]:
                aciertos.append("Culpable")
            if respuesta_lugar == juego.historia_actual["lugar"]:
                aciertos.append("Lugar")
            if respuesta_arma == juego.historia_actual["arma"]:
                aciertos.append("Arma")
            aciertos_str = ", ".join(aciertos) if aciertos else "ninguno"
            messagebox.showinfo("Resultado", "Lo siento, no has adivinado correctamente. Acertaste en: {}".format(aciertos_str), parent=ventana_adivinanza)

            
    
    ventana_adivinanza = tk.Toplevel(ventana)
    ventana_adivinanza.title("Adivinanza Final")
    
    tk.Label(ventana_adivinanza, text="¿Quién es el culpable?").pack()
    seleccion_opcion_culpable.set("")
    menu_culpable = tk.OptionMenu(ventana_adivinanza, seleccion_opcion_culpable, *juego.personajes)
    menu_culpable.pack()
    
    tk.Label(ventana_adivinanza, text="¿Dónde ocurrió el asesinato?").pack()
    seleccion_opcion_lugar.set("")
    menu_lugar = tk.OptionMenu(ventana_adivinanza, seleccion_opcion_lugar, *juego.lugares)
    menu_lugar.pack()
    
    tk.Label(ventana_adivinanza, text="¿Con qué arma?").pack()
    seleccion_opcion_arma.set("")
    menu_arma = tk.OptionMenu(ventana_adivinanza, seleccion_opcion_arma, *juego.armas)
    menu_arma.pack()
    
    boton_comprobar = tk.Button(ventana_adivinanza, text="Comprobar", command=comprobar_adivinanza)
    boton_comprobar.pack()
    
def reiniciar_juego():
    global juego
    juego = ClueJuego()
    mostrar_solucion()
    etiqueta_pistas_restantes.config(text="Pistas restantes: {}".format(juego.pistas_restantes))
    seleccion_tipo_pista.set("personaje")
    seleccion_opcion.set("")
    actualizar_lista()
    boton_reiniciar.grid(row=2, column=0, columnspan=2, pady=5)
    boton_pista.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    boton_pista.config(state=tk.NORMAL)
    
def confirmar_reinicio():
    confirmar = messagebox.askyesno("Confirmar reinicio", "¿Estás seguro de que quieres comenzar un nuevo juego?")
    if confirmar:
        reiniciar_juego()
    
def mostrar_solucion():
    # Mostrar solución del caso actual
    print("\n\n\t\tSolución del caso actual:")
    print(f"Culpable: {juego.historia_actual['culpable']}")
    print(f"Lugar del asesinato: {juego.historia_actual['lugar']}")
    print(f"Arma utilizada: {juego.historia_actual['arma']}")


# Configuración inicial del juego
juego = ClueJuego()
#guardar_historias_en_json(juego.historias)
mostrar_solucion()

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("900x600") 
ventana.title("Clue: Encuentra al asesino")

# Cambiar el ícono de la ventana
ruta_imagen_icono = "logo.ico"  # Ruta al archivo .ico

# Establecer el ícono de la ventana
ventana.iconbitmap(ruta_imagen_icono)

# Configurar la imagen de fondo
ruta_imagen_fondo = "Tab.png"

if not os.path.exists(ruta_imagen_fondo):
    tk.messagebox.showerror("Error", f"No se encontró la imagen:\n{ruta_imagen_fondo}")
    ventana.destroy()
else:
    print("Imagen encontrada: ", ruta_imagen_fondo)  # Para confirmar que se encuentra correctamente
    imagen_fondo = Image.open(ruta_imagen_fondo)
    imagen_fondo = imagen_fondo.resize((900, 600), Image.Resampling.LANCZOS)
    imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

    # Referencia a la imagen
    etiqueta_fondo = tk.Label(ventana, image=imagen_fondo_tk)
    etiqueta_fondo.image = imagen_fondo_tk
    etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Crear los widgets de la interfaz sobre la imagen de fondo
frame = tk.Frame(ventana, bg="white")
frame.pack(padx=20, pady=20)

etiqueta_tipo_pista = tk.Label(frame, text="Selecciona el tipo de pista:", bg="white")
etiqueta_tipo_pista.grid(row=0, column=0, padx=5, pady=5)
seleccion_tipo_pista = tk.StringVar()
seleccion_tipo_pista.set("personaje")
lista_tipos = tk.OptionMenu(frame, seleccion_tipo_pista, "personaje", "lugar", "arma")
lista_tipos.grid(row=0, column=1, padx=5, pady=5)

seleccion_tipo_pista.trace("w", actualizar_lista)

etiqueta_opcion = tk.Label(frame, text="Selecciona una opción:", bg="white")
etiqueta_opcion.grid(row=1, column=0, padx=5, pady=5)
seleccion_opcion = tk.StringVar()
lista_opciones = tk.OptionMenu(frame, seleccion_opcion, "")
lista_opciones.grid(row=1, column=1, padx=5, pady=5)

boton_reiniciar = tk.Button(frame, text="Nuevo Juego", command=confirmar_reinicio)
boton_reiniciar.grid(row=2, column=0, columnspan=2, pady=5)

boton_pista = tk.Button(frame, text="Mostrar Pista", command=mostrar_pista)
boton_pista.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

etiqueta_pistas_restantes = tk.Label(frame, text="Pistas restantes: {}".format(juego.pistas_restantes), bg="white")
etiqueta_pistas_restantes.grid(row=4, column=0, columnspan=2, padx=5, pady=5)


def cerrar_ventana():
    pygame.mixer.music.stop()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)
# Iniciar la interfaz
ventana.mainloop()
