# src/aprendizaje/aprendizaje.py

class Aprendizaje:
    """
    Clase encargada de modificar los pesos de los movimientos.

    Esta clase recibe el árbol AVL y actualiza los pesos
    dependiendo del resultado de la partida.
    """

    def __init__(self, arbol_movimientos):
        self.arbol_movimientos = arbol_movimientos
        self.iteraciones = 0
        self.victorias_programa = 0
        self.derrotas_programa = 0
        self.empates = 0

        # Guarda en qué iteración el programa ganó por primera vez.
        # Si todavía no ha ganado, se mantiene en None.
        self.primera_victoria_en = None

    def aprender_de_partida(self, resultado, jugadas_programa):
        """
        Ajusta los pesos de los movimientos usados por el programa.

        Esta versión permite aprendizaje progresivo:
        - Si gana, sube poco el peso.
        - Si pierde, baja poco.
        - Si empata, sube muy poco o se mantiene.
        """

        if resultado == "PROGRAMA":
            cambio = 1
            self.victorias_programa += 1

            if self.primera_victoria_en is None:
                self.primera_victoria_en = self.iteraciones + 1

        elif resultado == "HUMANO":
            cambio = -1
            self.derrotas_programa += 1

        else:
            cambio = 0
            self.empates += 1

        actual = jugadas_programa.cabeza

        while actual is not None:
            posicion = actual.dato
            self.arbol_movimientos.modificar_peso(posicion, cambio)
            actual = actual.siguiente

        self.iteraciones += 1

    def obtener_texto_estadisticas(self):
        """
        Retorna las estadísticas como texto.

        Esto nos servirá para mostrar en pantalla y también
        para guardar reportes.
        """
        texto = ""
        texto += "===================================\n"
        texto += "      ESTADÍSTICAS DE APRENDIZAJE  \n"
        texto += "===================================\n"
        texto += f"Iteraciones realizadas: {self.iteraciones}\n"
        texto += f"Victorias del programa: {self.victorias_programa}\n"
        texto += f"Derrotas del programa: {self.derrotas_programa}\n"
        texto += f"Empates: {self.empates}\n"

        if self.primera_victoria_en is None:
            texto += "Primera victoria del programa: todavía no ha ganado.\n"
        else:
            texto += f"Primera victoria del programa en la iteración: {self.primera_victoria_en}\n"

        texto += "===================================\n"

        return texto

    def mostrar_estadisticas(self):
        """
        Muestra un resumen del aprendizaje.
        """
        print()
        print(self.obtener_texto_estadisticas())