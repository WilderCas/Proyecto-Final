from src.estructuras.arbol_b import ArbolB, Partida


class HistorialPartidas:
    """
    Clase que administra el historial de partidas.

    Internamente usa un Árbol B.
    """

    def __init__(self, grado_arbol_b=2):
        self.arbol_b = ArbolB(grado_arbol_b)
        self.contador_partidas = 0

    def registrar_partida(self, resultado, tablero_final, jugadas_realizadas):
        """
        Crea una partida y la guarda en el Árbol B.
        """

        self.contador_partidas += 1

        resumen = self.crear_resumen(resultado, jugadas_realizadas)

        nueva_partida = Partida(
            self.contador_partidas,
            resultado,
            resumen,
            tablero_final
        )

        self.arbol_b.insertar(nueva_partida)

        return self.contador_partidas

    def crear_resumen(self, resultado, jugadas_realizadas):
        """
        Crea un resumen breve de la partida.

        Para no hacerlo demasiado largo, contamos cuántas jugadas hubo.
        """

        cantidad_jugadas = jugadas_realizadas.tamano

        resumen = f"Partida finalizada con resultado {resultado}. "
        resumen += f"Cantidad de jugadas realizadas: {cantidad_jugadas}."

        return resumen

    def mostrar_historial(self):
        """
        Muestra todas las partidas guardadas.
        """
        self.arbol_b.mostrar_historial()

    def buscar_partida(self, id_partida):
        """
        Busca una partida por ID.
        """
        return self.arbol_b.buscar(id_partida)

    def limpiar(self):
        """
        Limpia el historial completo.
        """
        self.arbol_b.limpiar()
        self.contador_partidas = 0