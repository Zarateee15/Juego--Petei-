import datos_juego.juego as j
import datos_juego.jugador as ju
from interfaces.interfaz_usuario import InterfazUsuario

'''
Este código define una aplicación de juego de cartas que utiliza una interfaz de consola para interactuar con el usuario. Los pasos básicos son:
    - Mostrar la portada del juego.
    - Solicitar el número de jugadores.
    - Solicitar los nombres de los jugadores.
    - Crear los jugadores y el juego.
    - Repartir 7 cartas a cada jugador.
    - Iniciar el juego.

'''
class App:
    @staticmethod
    
    def iniciar_juego():
        InterfazUsuario.mostrar_portada()
        num_jugadores = InterfazUsuario.solicitar_num_jugadores()
        nombres = InterfazUsuario.solicitar_nombres_jugadores(num_jugadores)

        jugadores = [ju.Jugador(nombre) for nombre in nombres]
        juego = j.JuegoPetei(jugadores)

        for _ in range(7):
            for jugador in jugadores:
                jugador.robar_carta(juego.mazo)

        juego.jugar()

app = App()
app.iniciar_juego()