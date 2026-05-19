class Jugador:
    """
    Clase que representa a un jugador del Totito.

    Atributos:
    - nombre: nombre del jugador.
    - simbolo: puede ser X o O.
    - tipo: puede ser HUMANO o PROGRAMA.
    """

    def __init__(self, nombre, simbolo, tipo):
        self.nombre = nombre
        self.simbolo = simbolo
        self.tipo = tipo

    def mostrar_info(self):
        """
        Muestra la información del jugador.
        """
        print(f"Jugador: {self.nombre}")
        print(f"Símbolo: {self.simbolo}")
        print(f"Tipo: {self.tipo}")