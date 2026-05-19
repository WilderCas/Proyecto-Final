class Movimiento:
    """
    Esta clase representa un movimiento posible del juego.

    Atributos:
    - posicion: número de casilla del tablero, de 0 a 8.
    - peso: valor que indica qué tan buena considera el programa esa posición.
    """

    def __init__(self, posicion, peso):
        self.posicion = posicion
        self.peso = peso

    def mostrar(self):
        """
        Retorna el movimiento como texto.
        """
        return f"Posición: {self.posicion} | Peso: {self.peso}"


class NodoAVL:
    """
    Nodo del árbol AVL.

    Cada nodo guarda un Movimiento.
    """

    def __init__(self, movimiento):
        self.movimiento = movimiento
        self.izquierda = None
        self.derecha = None
        self.altura = 1


class ArbolAVL:
    """
    Árbol AVL para guardar los movimientos posibles del programa.

    El árbol se ordena por la posición del movimiento.
    Ejemplo:
    posición 0, posición 1, posición 2, etc.

    El peso sirve para que el programa decida qué movimiento conviene más.
    """

    def __init__(self):
        self.raiz = None

    def obtener_altura(self, nodo):
        """
        Retorna la altura de un nodo.

        Si el nodo no existe, su altura es 0.
        """
        if nodo is None:
            return 0

        return nodo.altura

    def obtener_balance(self, nodo):
        """
        Calcula el balance de un nodo.

        balance = altura izquierda - altura derecha
        """
        if nodo is None:
            return 0

        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)

    def actualizar_altura(self, nodo):
        """
        Actualiza la altura de un nodo según sus hijos.
        """
        altura_izquierda = self.obtener_altura(nodo.izquierda)
        altura_derecha = self.obtener_altura(nodo.derecha)

        if altura_izquierda > altura_derecha:
            nodo.altura = altura_izquierda + 1
        else:
            nodo.altura = altura_derecha + 1

    def rotacion_derecha(self, nodo_desbalanceado):
        """
        Realiza una rotación simple a la derecha.

        Se usa cuando el árbol está cargado hacia la izquierda.
        """
        nueva_raiz = nodo_desbalanceado.izquierda
        subarbol_temporal = nueva_raiz.derecha

        nueva_raiz.derecha = nodo_desbalanceado
        nodo_desbalanceado.izquierda = subarbol_temporal

        self.actualizar_altura(nodo_desbalanceado)
        self.actualizar_altura(nueva_raiz)

        return nueva_raiz

    def rotacion_izquierda(self, nodo_desbalanceado):
        """
        Realiza una rotación simple a la izquierda.

        Se usa cuando el árbol está cargado hacia la derecha.
        """
        nueva_raiz = nodo_desbalanceado.derecha
        subarbol_temporal = nueva_raiz.izquierda

        nueva_raiz.izquierda = nodo_desbalanceado
        nodo_desbalanceado.derecha = subarbol_temporal

        self.actualizar_altura(nodo_desbalanceado)
        self.actualizar_altura(nueva_raiz)

        return nueva_raiz

    def insertar(self, posicion, peso):
        """
        Inserta un movimiento dentro del árbol AVL.
        """
        movimiento = Movimiento(posicion, peso)
        self.raiz = self._insertar_recursivo(self.raiz, movimiento)

    def _insertar_recursivo(self, nodo_actual, movimiento):
        """
        Inserta recursivamente y luego balancea el árbol.
        """
        if nodo_actual is None:
            return NodoAVL(movimiento)

        if movimiento.posicion < nodo_actual.movimiento.posicion:
            nodo_actual.izquierda = self._insertar_recursivo(nodo_actual.izquierda, movimiento)

        elif movimiento.posicion > nodo_actual.movimiento.posicion:
            nodo_actual.derecha = self._insertar_recursivo(nodo_actual.derecha, movimiento)

        else:
            # Si la posición ya existe, solo actualizamos el peso.
            nodo_actual.movimiento.peso = movimiento.peso
            return nodo_actual

        self.actualizar_altura(nodo_actual)

        balance = self.obtener_balance(nodo_actual)

        # Caso izquierda - izquierda
        if balance > 1 and movimiento.posicion < nodo_actual.izquierda.movimiento.posicion:
            return self.rotacion_derecha(nodo_actual)

        # Caso derecha - derecha
        if balance < -1 and movimiento.posicion > nodo_actual.derecha.movimiento.posicion:
            return self.rotacion_izquierda(nodo_actual)

        # Caso izquierda - derecha
        if balance > 1 and movimiento.posicion > nodo_actual.izquierda.movimiento.posicion:
            nodo_actual.izquierda = self.rotacion_izquierda(nodo_actual.izquierda)
            return self.rotacion_derecha(nodo_actual)

        # Caso derecha - izquierda
        if balance < -1 and movimiento.posicion < nodo_actual.derecha.movimiento.posicion:
            nodo_actual.derecha = self.rotacion_derecha(nodo_actual.derecha)
            return self.rotacion_izquierda(nodo_actual)

        return nodo_actual

    def buscar(self, posicion):
        """
        Busca un movimiento por posición.
        """
        return self._buscar_recursivo(self.raiz, posicion)

    def _buscar_recursivo(self, nodo_actual, posicion):
        """
        Búsqueda recursiva dentro del árbol.
        """
        if nodo_actual is None:
            return None

        if posicion == nodo_actual.movimiento.posicion:
            return nodo_actual.movimiento

        if posicion < nodo_actual.movimiento.posicion:
            return self._buscar_recursivo(nodo_actual.izquierda, posicion)

        return self._buscar_recursivo(nodo_actual.derecha, posicion)

    def modificar_peso(self, posicion, cambio):
        """
        Modifica el peso de un movimiento.

        cambio puede ser positivo o negativo.
        Ejemplo:
        +2 si el programa ganó.
        -1 si el programa perdió.
        """
        movimiento = self.buscar(posicion)

        if movimiento is not None:
            movimiento.peso += cambio

            # Evitamos que el peso sea negativo.
            if movimiento.peso < 0:
                movimiento.peso = 0

            return True

        return False

    def elegir_mejor_movimiento_disponible(self, tablero):
        """
        Busca dentro del árbol AVL el movimiento disponible con mayor peso.

        Recibe el tablero porque necesita saber qué posiciones están libres.
        """
        mejor_movimiento = self._buscar_mejor_recursivo(self.raiz, tablero, None)

        if mejor_movimiento is None:
            return None

        return mejor_movimiento.posicion

    def _buscar_mejor_recursivo(self, nodo_actual, tablero, mejor_movimiento):
        """
        Recorre el árbol para encontrar el mejor movimiento disponible.
        """
        if nodo_actual is None:
            return mejor_movimiento

        movimiento_actual = nodo_actual.movimiento

        if tablero.posicion_disponible(movimiento_actual.posicion):
            if mejor_movimiento is None:
                mejor_movimiento = movimiento_actual
            elif movimiento_actual.peso > mejor_movimiento.peso:
                mejor_movimiento = movimiento_actual

        mejor_movimiento = self._buscar_mejor_recursivo(nodo_actual.izquierda, tablero, mejor_movimiento)
        mejor_movimiento = self._buscar_mejor_recursivo(nodo_actual.derecha, tablero, mejor_movimiento)

        return mejor_movimiento

    def mostrar_inorden(self):
        """
        Muestra los movimientos ordenados por posición.
        """
        print("Movimientos registrados en el Árbol AVL:")
        self._mostrar_inorden_recursivo(self.raiz)

    def _mostrar_inorden_recursivo(self, nodo_actual):
        """
        Recorrido inorden del árbol AVL.
        """
        if nodo_actual is not None:
            self._mostrar_inorden_recursivo(nodo_actual.izquierda)
            print(nodo_actual.movimiento.mostrar())
            self._mostrar_inorden_recursivo(nodo_actual.derecha)

    def cargar_movimientos_iniciales(self):
        """
        Inserta las 9 posiciones del tablero en el árbol.

        Le damos más peso inicial al centro y a las esquinas,
        porque normalmente son mejores posiciones en Totito.
        """
        self.insertar(0, 3)
        self.insertar(1, 1)
        self.insertar(2, 3)
        self.insertar(3, 1)
        self.insertar(4, 5)
        self.insertar(5, 1)
        self.insertar(6, 3)
        self.insertar(7, 1)
        self.insertar(8, 3)

    def reiniciar(self):
        """
        Limpia el árbol y vuelve a cargar los movimientos iniciales.
        """
        self.raiz = None
        self.cargar_movimientos_iniciales()