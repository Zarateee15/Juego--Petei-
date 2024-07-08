import tkinter as tk    # Para interfaces gráficas
from tkinter import messagebox  # Cuadros de dialogos
from datos_juego.persistencia import cargar_estado, guardar_estado
from datos_juego.juego import JuegoPetei
from datos_juego.jugador import Jugador
from datos_juego.carta import CartaCambioColor, CartaMasCuatro

'''
Esta clase proporciona una interfaz gráfica para el juego de cartas, permitiendo a los 
usuarios interactuar con el juego de manera visual, gestionar el estado del juego, y 
realizar acciones como jugar cartas, robar cartas y elegir colores para cartas especiales.

'''
class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Cartas")
        
        # Inicializa la interfaz y carga una partida existente o inicia una nueva.
        self.inicializar_interfaz()
        self.cargar_o_nueva_partida()

    # Configura la interfaz inicial con etiquetas y botones para seleccionar el número de jugadores.
    def inicializar_interfaz(self):
        self.portada = tk.Label(self.root, text="¡Bienvenido a Petei!", font=("Helvetica", 16))
        self.portada.pack(pady=20)

        self.num_jugadores_label = tk.Label(self.root, text="Seleccione el número de jugadores:", font=("Helvetica", 12))
        self.num_jugadores_label.pack(pady=10)

        self.num_jugadores_frame = tk.Frame(self.root)
        self.num_jugadores_frame.pack(pady=10)

        for i in range(2, 11):
            button = tk.Button(self.num_jugadores_frame, text=str(i), command=lambda i=i: self.solicitar_nombres_jugadores(i))
            button.pack(side=tk.LEFT, padx=5)

    # Pregunta si se desea cargar una partida guardada o iniciar una nueva.
    def cargar_o_nueva_partida(self):
        if cargar_estado():
            if messagebox.askyesno("Cargar Partida", "¿Desea cargar la partida guardada?"):
                self.juego = cargar_estado()
                self.jugadores = self.juego.jugadores
                self.mostrar_cartas_jugador()
            else:
                self.iniciar_interfaz_nueva_partida()
        else:
            self.iniciar_interfaz_nueva_partida()

    # Muestra los elementos de la interfaz para iniciar una nueva partida.
    def iniciar_interfaz_nueva_partida(self):
        self.portada.pack()
        self.num_jugadores_label.pack()
        self.num_jugadores_frame.pack()

    # Almacena el número de jugadores y llama a la función para solicitar los nombres.
    def solicitar_nombres_jugadores(self, num_jugadores):
        self.num_jugadores = num_jugadores
        self.mostrar_nombres_jugadores()

    # Muestra campos de entrada para los nombres de los jugadores y un botón para iniciar el juego.
    def mostrar_nombres_jugadores(self):
        self.portada.pack_forget()
        self.num_jugadores_label.pack_forget()
        self.num_jugadores_frame.pack_forget()

        self.nombres_jugadores = []

        for i in range(self.num_jugadores):
            label = tk.Label(self.root, text=f"Nombre del jugador {i + 1}:", font=("Helvetica", 12))
            label.pack(pady=5)
            entry = tk.Entry(self.root)
            entry.pack(pady=5)
            self.nombres_jugadores.append(entry)

        self.iniciar_juego_button = tk.Button(self.root, text="Iniciar Juego", command=self.iniciar_juego)
        self.iniciar_juego_button.pack(pady=20)

    # Valida los nombres de los jugadores, inicializa el juego y reparte las cartas iniciales.
    def iniciar_juego(self):
        nombres = [entry.get().strip() for entry in self.nombres_jugadores]
        if all(nombres):
            self.jugadores = [Jugador(nombre) for nombre in nombres]
            self.juego = JuegoPetei(self.jugadores)
            for _ in range(7):
                for jugador in self.jugadores:
                    jugador.robar_carta(self.juego.mazo)
            self.mostrar_cartas_jugador()
        else:
            messagebox.showerror("Error", "Todos los nombres deben estar llenos.")

    # Muestra las cartas del jugador actual y permite seleccionar una carta para jugar o robar una carta.
    def mostrar_cartas_jugador(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

        self.jugador_actual = self.juego.jugadores[self.juego.turno_actual]

        label = tk.Label(self.root, text=f"Turno de {self.jugador_actual.nombre}", font=("Helvetica", 16))
        label.pack(pady=10)

        carta_tope_label = tk.Label(self.root, text=f"Carta en el tope: {self.obtener_texto_carta(self.juego.pila_descartes[-1])}", font=("Helvetica", 14))
        carta_tope_label.pack(pady=10)

        self.cartas_frame = tk.Frame(self.root)
        self.cartas_frame.pack(pady=10)

        for i, carta in enumerate(self.jugador_actual.mano):
            if i % 7 == 0:
                fila_frame = tk.Frame(self.cartas_frame)
                fila_frame.pack()
            button = tk.Button(fila_frame, text=self.obtener_texto_carta(carta), command=lambda i=i: self.jugar_carta(i))
            button.pack(side=tk.LEFT, padx=5)

        robar_button = tk.Button(self.root, text="Robar Carta", command=self.robar_carta)
        robar_button.pack(pady=10)

    # Devuelve una representación de texto de la carta, con el valor y el color.
    def obtener_texto_carta(self, carta):
        if isinstance(carta, (CartaCambioColor, CartaMasCuatro)):
            return f"{carta.valor} ({carta.color})"
        return f"{carta.color} {carta.valor}"

    # Permite al jugador jugar una carta si es jugable, o solicita el color si es una carta especial.
    def jugar_carta(self, indice):
        carta = self.jugador_actual.mano[indice]
        if carta.es_jugable(self.juego.pila_descartes[-1]):
            if isinstance(carta, (CartaCambioColor, CartaMasCuatro)):
                self.solicitar_color(carta)
            else:
                self.jugador_actual.jugar_carta(carta, self.juego)
                self.actualizar_juego()
        else:
            messagebox.showerror("Error", "No puede jugar esa carta. Elija una opción válida.")

    # Abre una nueva ventana para que el jugador elija un color para una carta especial.
    def solicitar_color(self, carta):
        self.color_window = tk.Toplevel(self.root)
        self.color_window.title("Elija un color")

        label = tk.Label(self.color_window, text="Elija un color:", font=("Helvetica", 12))
        label.pack(pady=10)

        colores = [("rojo", "red"), ("amarillo", "yellow"), ("verde", "green"), ("azul", "blue")]
        for color_es, color_en in colores:
            button = tk.Button(self.color_window, text=color_es.capitalize(), bg=color_en, command=lambda c=color_es: self.elegir_color(c, carta))
            button.pack(pady=5, padx=5, fill=tk.X)

    # Establece el color elegido para la carta especial, aplica su efecto y actualiza el juego.
    def elegir_color(self, color, carta):
        carta.color = color
        carta.aplicar_efecto(self.juego, color)
        self.jugador_actual.jugar_carta(carta, self.juego)
        self.color_window.destroy()
        self.actualizar_juego()

    # Muestra el color elegido y actualiza la interfaz para continuar el juego. 
    def mostrar_color_elegido(self, color):
        for widget in self.root.winfo_children():
            widget.pack_forget()
        
        label = tk.Label(self.root, text=f"Color elegido: {color.capitalize()}", font=("Helvetica", 16))
        label.pack(pady=10)
        
        self.mostrar_cartas_jugador()

    # Permite al jugador robar una carta del mazo.
    def robar_carta(self):
        self.jugador_actual.robar_carta(self.juego.mazo)
        self.actualizar_juego()

    # Actualiza el estado del juego, verifica si hay un ganador y guarda el estado del juego.
    def actualizar_juego(self):
        if len(self.jugador_actual.mano) == 0:
            messagebox.showinfo("Ganador", f"{self.jugador_actual.nombre} ha ganado!")
            guardar_estado(self.juego)  # Guardar estado al finalizar el juego
            self.root.quit()
        else:
            self.juego.saltar_turno()
            self.mostrar_cartas_jugador()

# Crea la ventana principal y ejecuta la aplicación.
if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()

    # Guardar estado del juego al salir de la aplicación
    guardar_estado(app.juego)
