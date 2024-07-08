from abc import ABC, abstractmethod
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Define una carta genérica en el juego con un color y un valor.
class Carta(ABC):
    # Constructor que inicializa una carta con un color y un valor dados.
    def __init__(self, color, valor):
        self.color = color
        self.valor = valor

    # Método especial que devuelve una representación en cadena de la carta.
    def __str__(self):
        color_code = {
            "rojo": Fore.RED,
            "amarillo": Fore.YELLOW,
            "verde": Fore.GREEN,
            "azul": Fore.BLUE,
            "comodin": Fore.MAGENTA
        }
        return f"{color_code.get(self.color, '')}{self.color} {self.valor}{Style.RESET_ALL}"

    #  Método que verifica si la carta actual es jugable sobre la carta en la cima de la pila de descartes.
    def es_jugable(self, carta_tope):
        return self.color == carta_tope.color or self.valor == carta_tope.valor or self.color == "comodin"

    # Método abstracto que define cómo se aplica el efecto de una carta en el juego.
    @abstractmethod
    def aplicar_efecto(self, juego):
        pass

# Representa una carta numérica específica.
class CartaNumero(Carta):
    def __init__(self, color, numero):
        super().__init__(color, str(numero))

    def aplicar_efecto(self, juego):
        pass  # Las cartas de número no tienen un efecto especial

# Representa una carta especial (como Salto, Reversa, +2, etc.).
class CartaEspecial(Carta):
    def __init__(self, color, tipo):
        super().__init__(color, tipo)
        
        
# Cada una de estas clases representa un tipo específico de carta especial con su propio efecto único.

# Bloquea el turno de la siguiente persona
class CartaSalto(CartaEspecial):
    def __init__(self, color):
        super().__init__(color, "salto")

    def aplicar_efecto(self, juego):
        juego.turno_actual = (juego.turno_actual + 1) % len(juego.jugadores)
        

# Invierte la dirección del juego.
class CartaReversa(CartaEspecial):
    def __init__(self, color):
        super().__init__(color, "reversa")

    def aplicar_efecto(self, juego):
        juego.reversar_direccion()

# Hace que el siguiente jugador robe 2 cartas
class CartaMasDos(CartaEspecial):
    def __init__(self, color):
        super().__init__(color, "+2")

    def aplicar_efecto(self, juego):
        juego.dar_cartas(2)

# Cambia el color
class CartaCambioColor(CartaEspecial):
    def __init__(self):
        super().__init__("comodin", "cambio color")

    def aplicar_efecto(self, juego, color=None):
        if color:
            juego.pila_descartes[-1].color = color

# El siguiente jugador roba 4 cartas
class CartaMasCuatro(CartaEspecial):
    def __init__(self):
        super().__init__("comodin", "+4")

    def aplicar_efecto(self, juego, color=None):
        juego.dar_cartas(2)
        if color:
            juego.pila_descartes[-1].color = color
            
    