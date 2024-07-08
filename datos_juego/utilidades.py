import os

# Método que limpia la pantalla de la terminal
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
