# src/juego/tablero.py

from src.estructuras.lista_enlazada import ListaEnlazada


class Tablero:
    """
    Clase que representa el tablero de Totito.

    El tablero normalmente se podría representar con una matriz 3x3,
    pero por las restricciones del proyecto usamos una lista enlazada propia.

    Posiciones del tablero:

        0 | 1 | 2
       ---+---+---
        3 | 4 | 5
       ---+---+---
        6 | 7 | 8
    """

    def __init__(self):
        self.casillas = ListaEnlazada()
        self.inicializar_tablero()

    def inicializar_tablero(self):
        """
        Crea las 9 casillas vacías del tablero.
        """
        self.casillas.limpiar()

        contador = 0

        while contador < 9:
            self.casillas.agregar_final(" ")
            contador += 1

    def mostrar_tablero(self):
        """
        Muestra el tablero en consola.
        """
        print()
        print("     0   1   2")
        print("   -----------")
        print(f"0 |  {self.obtener_casilla(0)} | {self.obtener_casilla(1)} | {self.obtener_casilla(2)}")
        print("   -----------")
        print(f"1 |  {self.obtener_casilla(3)} | {self.obtener_casilla(4)} | {self.obtener_casilla(5)}")
        print("   -----------")
        print(f"2 |  {self.obtener_casilla(6)} | {self.obtener_casilla(7)} | {self.obtener_casilla(8)}")
        print("   -----------")
        print()

    def obtener_casilla(self, posicion):
        """
        Retorna el valor de una casilla.
        """
        return self.casillas.obtener_por_indice(posicion)

    def colocar_simbolo(self, posicion, simbolo):
        """
        Coloca X u O en una posición si está vacía.

        Retorna:
        True si se pudo colocar.
        False si la posición no es válida o ya está ocupada.
        """
        if posicion < 0 or posicion > 8:
            return False

        valor_actual = self.obtener_casilla(posicion)

        if valor_actual != " ":
            return False

        self.casillas.modificar_por_indice(posicion, simbolo)
        return True

    def posicion_disponible(self, posicion):
        """
        Verifica si una posición está vacía.
        """
        if posicion < 0 or posicion > 8:
            return False

        return self.obtener_casilla(posicion) == " "

    def tablero_lleno(self):
        """
        Verifica si ya no hay espacios disponibles.
        """
        posicion = 0

        while posicion < 9:
            if self.obtener_casilla(posicion) == " ":
                return False

            posicion += 1

        return True

    def obtener_estado_como_texto(self):
        """
        Retorna el estado del tablero como texto.

        Esto nos servirá más adelante para guardar el historial
        en el árbol B.
        """
        texto = ""

        posicion = 0

        while posicion < 9:
            valor = self.obtener_casilla(posicion)

            if valor == " ":
                texto += "-"
            else:
                texto += valor

            posicion += 1

        return texto

    def reiniciar(self):
        """
        Limpia el tablero para iniciar una nueva partida.
        """
        self.inicializar_tablero()