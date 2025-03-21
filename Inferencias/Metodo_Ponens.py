# Metodo Ponens
# Preguntar al usuario si tiene fiebre
tiene_fiebre = input("¿Tienes fiebre? (sí/no): ").strip().lower()

# Validar la entrada y asignar valor booleano
if tiene_fiebre == "si":
    tiene_fiebre = True
else:
    tiene_fiebre = False

# Inicialmente no se ha diagnosticado gripe
tiene_gripe = False

# Aplicar Modus Ponens: Si tiene fiebre, se infiere que tiene gripe
if tiene_fiebre:
    tiene_gripe = True  # Inferimos que tiene gripe si tiene fiebre

# Resultado del diagnóstico
print("¿El paciente tiene gripe?", tiene_gripe)
