# src/historial/historial_partidas.py

from src.estructuras.arbol_b import ArbolB, Partida


class HistorialPartidas:
    """
    Clase que administra el historial de partidas.

    Internamente usa un Árbol B.
    """

    def __init__(self, grado_arbol_b=2):
        self.arbol_b = ArbolB(grado_arbol_b)
        self.contador_partidas = 0
        self.grado_arbol_b = grado_arbol_b

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
        """

        cantidad_jugadas = jugadas_realizadas.tamano

        resumen = f"Partida finalizada con resultado {resultado}. "
        resumen += f"Cantidad de jugadas realizadas: {cantidad_jugadas}."

        return resumen

    def mostrar_historial(self):
        """
        Muestra todas las partidas guardadas en consola.
        """
        self.arbol_b.mostrar_historial()

    def obtener_historial_como_texto(self):
        """
        Retorna todo el historial como texto.

        Este método sirve para mostrar el historial en Tkinter,
        porque mostrar_historial() solo imprime en consola.
        """

        texto = ""
        texto += "===================================\n"
        texto += "        HISTORIAL DE PARTIDAS      \n"
        texto += "===================================\n"
        texto += f"Grado mínimo del Árbol B: {self.grado_arbol_b}\n"
        texto += f"Máximo de claves por nodo: {(2 * self.grado_arbol_b) - 1}\n"
        texto += "===================================\n\n"

        if self.contador_partidas == 0:
            texto += "No hay partidas registradas."
            return texto

        texto = self._recorrer_arbol_b_texto(self.arbol_b.raiz, texto)

        return texto

    def _recorrer_arbol_b_texto(self, nodo, texto):
        """
        Recorre el Árbol B en orden y convierte las partidas a texto.
        """

        indice = 0

        while indice < len(nodo.partidas):
            if not nodo.hoja:
                texto = self._recorrer_arbol_b_texto(nodo.hijos[indice], texto)

            texto += "-----------------------------------\n"
            texto += nodo.partidas[indice].mostrar()
            texto += "\n"

            indice += 1

        if not nodo.hoja:
            texto = self._recorrer_arbol_b_texto(nodo.hijos[indice], texto)

        return texto

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