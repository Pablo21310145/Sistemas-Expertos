import json

# Base de datos inicial de preguntas y respuestas
knowledge_base = {
    "hola": "¡Hola! ¿Cómo estás?",
    "como estas?": "Estoy bien, gracias por preguntar.",
    "de que te gustaría hablar?": "¡Estoy aquí para hablar de lo que quieras!",
}

# Guardar la base de datos en un archivo para persistencia
def save_knowledge():
    with open("knowledge_base.json", "w") as file:
        json.dump(knowledge_base, file)

# Cargar la base de datos desde un archivo
def load_knowledge():
    try:
        with open("knowledge_base.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return knowledge_base  # Si no existe el archivo, usar la base predeterminada

# Función principal del chatbot
def chatbot():
    print("¡Hola! Soy tu chatbot. Escribe 'salir' para terminar.")
    
    while True:
        user_input = input("Tú: ").lower()

        if user_input == "salir":
            print("Adiós. ¡Hasta luego!")
            break

        # Verificar si la entrada del usuario está en la base de conocimientos
        if user_input in knowledge_base:
            print(f"Chatbot: {knowledge_base[user_input]}")
        else:
            print("Chatbot: No tengo una respuesta para eso.")
            # Pedir al usuario que ingrese una nueva pregunta y respuesta
            new_question = input("¿Qué debería responder a eso? ")
            knowledge_base[user_input] = new_question
            save_knowledge()  # Guardar la nueva respuesta en el archivo
            print("Chatbot: Gracias por ayudarme a aprender algo nuevo.")

if __name__ == "__main__":
    knowledge_base = load_knowledge()  # Cargar la base de datos
    chatbot()  # Iniciar el chatbot
