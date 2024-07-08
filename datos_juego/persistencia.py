import pickle

# Guarda el estado del juego en un archivo utilizando pickle.
def guardar_estado(juego, nombre_archivo='estado_juego.pkl'):
    with open(nombre_archivo, 'wb') as archivo:
        pickle.dump(juego, archivo)

# Carga el estado del juego desde un archivo utilizando pickle.
def cargar_estado(nombre_archivo='estado_juego.pkl'):
    try:
        with open(nombre_archivo, 'rb') as archivo:
            juego = pickle.load(archivo)
        return juego
    except FileNotFoundError:
        return None
