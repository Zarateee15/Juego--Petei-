from colorama import Fore, Style, init
import datos_juego.carta as c
import random
from interfaces.interfaz_usuario import InterfazUsuario

# Inicializar colorama
init(autoreset=True)

class JuegoPetei:
    # Constructor que inicializa el juego con una lista de jugadores.
    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.mazo = self.crear_mazo()
        self.pila_descartes = [self.mazo.pop()]
        self.direccion_normal = True
        self.turno_actual = 0
    
    # Método que crea el mazo con las 108 cartas del juego.
    def crear_mazo(self):
        colores = ["rojo", "amarillo", "verde", "azul"]
        mazo = []

        # Añade las cartas numéricas.
        for color in colores:
            mazo.append(c.CartaNumero(color, 0))
            for _ in range(2):
                for numero in range(1, 10):
                    mazo.append(c.CartaNumero(color, numero))

        # Añadir las cartas especiales.
        for color in colores:
            for _ in range(2):
                mazo.append(c.CartaSalto(color))
                mazo.append(c.CartaReversa(color))
                mazo.append(c.CartaMasDos(color))

        # Añadir los comodines.
        for _ in range(4):
            mazo.append(c.CartaCambioColor())
            mazo.append(c.CartaMasCuatro())

        random.shuffle(mazo)
        
        return mazo

    # Avanza al siguiente turno según la dirección actual del juego.
    def saltar_turno(self):
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)

    # Cambia la dirección del juego entre normal y reversa.
    def reversar_direccion(self):
        self.direccion_normal = not self.direccion_normal
        
    # Hace que el siguiente jugador roba una cantidad específica de cartas del mazo.
    def dar_cartas(self, cantidad):
        siguiente_jugador = (self.turno_actual + 1) % len(self.jugadores)
        for _ in range(cantidad):
            if self.mazo:
                self.jugadores[siguiente_jugador].robar_carta(self.mazo)
            else:
                print("No quedan cartas en el mazo.")

    # Imprime la cantidad de cartas restantes en el mazo.
    def mostrar_cartas_restantes(self):
        print(f"{Style.BRIGHT}{Fore.BLACK}CARTAS RESTANTES EN EL MAZO: {Fore.WHITE}{len(self.mazo)}{Style.RESET_ALL}\n")
        print(f"{Style.BRIGHT}{Fore.WHITE}----------------------------------------------------------------------------------{Style.RESET_ALL}")

    # Método principal que maneja la lógica del juego mientras no haya un ganador.
    def jugar(self):
        # Bucle hasta que alguien gane el juego
        while True:
            InterfazUsuario.mostrar_estado_juego(self)
            jugador_actual = self.jugadores[self.turno_actual]
            InterfazUsuario.mostrar_cartas_jugador(jugador_actual)
            carta_jugada = None

            while True:
                # Pide al jugador que elija una carta para jugar o que robe una carta.
                opcion = InterfazUsuario.solicitar_opcion_jugador()

                if opcion.lower() == 'r':
                    if self.mazo:
                        jugador_actual.robar_carta(self.mazo)
                        InterfazUsuario.mostrar_cartas_restantes(self)
                        break
                    else:
                        print("No quedan cartas en el mazo. Elige otra opción.")
                else:
                    # Verifica si el índice es válido y si la carta en ese índice es jugable.
                    try:
                        indice = int(opcion)
                        if 0 <= indice < len(jugador_actual.mano):
                            carta = jugador_actual.mano[indice]
                            if jugador_actual.jugar_carta(carta, self):
                                carta_jugada = carta
                                InterfazUsuario.mostrar_cartas_restantes(self)
                                break
                        else:
                            print(f"{Style.BRIGHT}{Fore.RED}Elija una opción válida. {Style.RESET_ALL}")
                    except ValueError:
                        print(f"{Style.BRIGHT}{Fore.RED}Elija una opción válida. {Style.RESET_ALL}")

            if len(jugador_actual.mano) == 0:
                InterfazUsuario.mostrar_ganador(jugador_actual)
                break

            if self.direccion_normal:
                self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
            else:
                self.turno_actual = (self.turno_actual - 1) % len(self.jugadores)
