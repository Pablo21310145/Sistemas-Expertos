# Metodo Tollens
# Preguntar al usuario si calificó la película como "buena"
calificacion_buena = input("¿Calificaste la película como buena? (sí/no): ").strip().lower()

# Validar la entrada y asignar valor booleano
if calificacion_buena == "si":
    calificacion_buena = True
else:
    calificacion_buena = False

# Inicialmente, se recomendó una película
pelicula_recomendada = True

# Aplicar Modus Tollens: Si no califica la película como "buena", entonces no es adecuada para el usuario
if not calificacion_buena:
    pelicula_recomendada = False  # Inferimos que la película no es adecuada

# Resultado de la recomendación
print("¿La película es adecuada para el usuario?", pelicula_recomendada)
