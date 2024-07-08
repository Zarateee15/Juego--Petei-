from colorama import Fore, Style, init
from datos_juego.utilidades import limpiar_pantalla

init(autoreset=True)

class InterfazUsuario:
    #  Limpia la pantalla y muestra la portada del juego 
    @staticmethod
    def mostrar_portada():
        limpiar_pantalla()
        print(f"{Style.BRIGHT}{Fore.CYAN}"
              '''
                 ______   _______  __________  _______   __         
                |   __ \ |   ____||____  ____||   ____| |  |      
                |  |__) ||  |___      |  |    |  |___   |  |         
                |   ___/ |   ___|     |  |    |   ___|  |  |   
                |  |     |  |____     |  |    |  |____  |  |
                |__|     |_______|    |__|    |_______| |__|       
                                                
                                                
              '''
              f"{Style.RESET_ALL}")

    # Solicita al usuario ingresar el número de jugadores (entre 2 y 10) y valida la entrada
    @staticmethod
    def solicitar_num_jugadores():
        while True:
            try:
                print(f"{Style.BRIGHT}{Fore.WHITE}----------------------------------------------------------------------------------{Style.RESET_ALL}")
                print(f"{Style.BRIGHT}{Fore.WHITE}Ingrese el número de jugadores (máximo 10): {Style.RESET_ALL}")
                num_jugadores = int(input())
                if 1 < num_jugadores <= 10:
                    return num_jugadores
                else:
                    print(f"{Style.BRIGHT}{Fore.RED}Elija una opción válida. {Style.RESET_ALL}")
            except ValueError:
                print(f"{Style.BRIGHT}{Fore.RED}Elija una opción válida. {Style.RESET_ALL}")

    # Solicita al usuario ingresar los nombres de los jugadores y los valida para no estar vacíos.
    @staticmethod
    def solicitar_nombres_jugadores(num_jugadores):
        nombres = []
        for i in range(num_jugadores):
            while True:
                print(f"{Style.BRIGHT}{Fore.WHITE}----------------------------------------------------------------------------------{Style.RESET_ALL}")
                print(f"{Style.BRIGHT}{Fore.WHITE}Ingresa el nombre del jugador {i + 1}: {Style.RESET_ALL}")
                nombre = input()
                if nombre.strip():  # Verifica si el nombre no está vacío después de quitar espacios en blanco
                    nombres.append(nombre)
                    break
                else:
                    print(f"{Style.BRIGHT}{Fore.RED}El nombre no puede estar vacío. {Style.RESET_ALL}")
        return nombres

    # Limpia la pantalla y muestra el estado actual del juego, incluyendo el turno del jugador actual y la carta en el tope de la pila de descartes.
    @staticmethod
    def mostrar_estado_juego(juego):
        limpiar_pantalla()
        jugador_actual = juego.jugadores[juego.turno_actual]
        print(f"{Style.BRIGHT}{Fore.WHITE}----------------------------------------------------------------------------------{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.CYAN}                              Turno de {jugador_actual.nombre}{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.WHITE}----------------------------------------------------------------------------------{Style.RESET_ALL}")
        print(f"\n{Style.BRIGHT}{Fore.BLACK}CARTA EN EL TOPE: {Style.RESET_ALL}{juego.pila_descartes[-1]}")
        InterfazUsuario.mostrar_cartas_restantes(juego)

    # Muestra cuántas cartas quedan en el mazo.
    @staticmethod
    def mostrar_cartas_restantes(juego):
        print(f"{Style.BRIGHT}{Fore.BLACK}CARTAS RESTANTES EN EL MAZO: {Fore.WHITE}{len(juego.mazo)}{Style.RESET_ALL}\n")
        print(f"{Style.BRIGHT}{Fore.WHITE}----------------------------------------------------------------------------------{Style.RESET_ALL}")

    # Muestra las cartas en la mano del jugador actual con sus respectivos índices.
    @staticmethod
    def mostrar_cartas_jugador(jugador):
        for i, carta in enumerate(jugador.mano):
            print(f"{i}: {carta}")

    # Solicita al jugador que elija una carta para jugar o que robe una carta del mazo.
    @staticmethod
    def solicitar_opcion_jugador():
        print(f"{Style.BRIGHT}{Fore.WHITE}----------------------------------------------------------------------------------{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.WHITE}Elija el índice de la carta que desee jugar o escriba 'R' para robar una carta del mazo: {Style.RESET_ALL}")
        return input()

    # Limpia la pantalla y muestra un mensaje indicando que el jugador ha ganado el juego.
    @staticmethod
    def mostrar_ganador(jugador):
        limpiar_pantalla()
        print(f"{Style.BRIGHT}{Fore.WHITE}----------------------------------------------------------------------------------{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.CYAN}                              {jugador.nombre} ha ganado!{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.WHITE}----------------------------------------------------------------------------------{Style.RESET_ALL}")
