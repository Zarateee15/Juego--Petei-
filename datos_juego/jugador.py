from colorama import Fore, Style, init
import datos_juego.carta as c

# Inicializar colorama
init(autoreset=True)

# Clase que representa a cada jugador del juego
class Jugador:
    # Constructor que inicializa un jugador con un nombre y una lista vacía, que representa las cartas que tiene en la mano.
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []

    # Método que permite al jugador robar una carta del mazo.
    def robar_carta(self, mazo):
        if mazo:
            self.mano.append(mazo.pop())
        else:
            print("No quedan cartas en el mazo para robar.")

    # Método para que el jugador juegue una carta en el juego.
    def jugar_carta(self, carta, juego):
        if carta.es_jugable(juego.pila_descartes[-1]):
            self.mano.remove(carta)
            juego.pila_descartes.append(carta)
            if isinstance(carta, c.CartaEspecial):
                carta.aplicar_efecto(juego)
            return True
        else:
            print(f"{Style.BRIGHT}{Fore.RED}No puede jugar esa carta. Elija una opción válida. {Style.RESET_ALL}")
            return False

    # Método que devuelve una cadena incluyendo al jugador y las cartas que tiene en la mano.
    def __str__(self):
        return f"{self.nombre}: {' '.join(str(carta) for carta in self.mano)}"