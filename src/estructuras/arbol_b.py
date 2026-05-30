class Partida:
    """
    Representa una partida jugada.

    Atributos:
    - id_partida: identificador único de la partida.
    - resultado: puede ser PROGRAMA, HUMANO o EMPATE.
    - resumen: descripción breve de la partida.
    - tablero_final: estado final del tablero en texto.
    """

    def __init__(self, id_partida, resultado, resumen, tablero_final):
        self.id_partida = id_partida
        self.resultado = resultado
        self.resumen = resumen
        self.tablero_final = tablero_final

    def mostrar(self):
        """
        Retorna la información de la partida como texto.
        """
        texto = ""
        texto += f"ID Partida: {self.id_partida}\n"
        texto += f"Resultado: {self.resultado}\n"
        texto += f"Resumen: {self.resumen}\n"
        texto += f"Tablero final: {self.tablero_final}\n"
        return texto


class NodoB:
    """
    Nodo del Árbol B.

    Cada nodo guarda:
    - partidas: partidas almacenadas en el nodo.
    - hijos: referencias a otros nodos.
    - hoja: indica si el nodo no tiene hijos.
    """

    def __init__(self, hoja=True):
        self.partidas = []
        self.hijos = []
        self.hoja = hoja


class ArbolB:
    """
    Árbol B para guardar el historial de partidas.

    El grado mínimo se puede configurar.
    Si grado_minimo = 2, cada nodo puede tener como máximo 3 claves.

    Fórmula:
    máximo de claves = 2 * grado_minimo - 1
    """

    def __init__(self, grado_minimo=2):
        self.raiz = NodoB(True)
        self.grado_minimo = grado_minimo

    def insertar(self, partida):
        """
        Inserta una partida dentro del árbol B.
        """

        raiz_actual = self.raiz

        maximo_claves = (2 * self.grado_minimo) - 1

        if len(raiz_actual.partidas) == maximo_claves:
            nueva_raiz = NodoB(False)
            nueva_raiz.hijos.append(raiz_actual)

            self.dividir_hijo(nueva_raiz, 0)

            self.raiz = nueva_raiz
            self.insertar_no_lleno(nueva_raiz, partida)
        else:
            self.insertar_no_lleno(raiz_actual, partida)

    def insertar_no_lleno(self, nodo, partida):
        """
        Inserta una partida en un nodo que todavía tiene espacio.
        """

        indice = len(nodo.partidas) - 1

        if nodo.hoja:
            nodo.partidas.append(None)

            while indice >= 0 and partida.id_partida < nodo.partidas[indice].id_partida:
                nodo.partidas[indice + 1] = nodo.partidas[indice]
                indice -= 1

            nodo.partidas[indice + 1] = partida

        else:
            while indice >= 0 and partida.id_partida < nodo.partidas[indice].id_partida:
                indice -= 1

            indice += 1

            maximo_claves = (2 * self.grado_minimo) - 1

            if len(nodo.hijos[indice].partidas) == maximo_claves:
                self.dividir_hijo(nodo, indice)

                if partida.id_partida > nodo.partidas[indice].id_partida:
                    indice += 1

            self.insertar_no_lleno(nodo.hijos[indice], partida)

    def dividir_hijo(self, nodo_padre, indice_hijo):
        """
        Divide un hijo lleno en dos nodos.

        Este es el proceso principal del Árbol B:
        cuando un nodo se llena, se parte y la clave del medio sube.
        """

        grado = self.grado_minimo
        nodo_lleno = nodo_padre.hijos[indice_hijo]
        nodo_nuevo = NodoB(nodo_lleno.hoja)

        partida_media = nodo_lleno.partidas[grado - 1]

        nodo_nuevo.partidas = nodo_lleno.partidas[grado:]
        nodo_lleno.partidas = nodo_lleno.partidas[:grado - 1]

        if not nodo_lleno.hoja:
            nodo_nuevo.hijos = nodo_lleno.hijos[grado:]
            nodo_lleno.hijos = nodo_lleno.hijos[:grado]

        nodo_padre.hijos.insert(indice_hijo + 1, nodo_nuevo)
        nodo_padre.partidas.insert(indice_hijo, partida_media)

    def buscar(self, id_partida):
        """
        Busca una partida por su ID.
        """
        return self._buscar_recursivo(self.raiz, id_partida)

    def _buscar_recursivo(self, nodo, id_partida):
        """
        Búsqueda recursiva dentro del árbol B.
        """

        indice = 0

        while indice < len(nodo.partidas) and id_partida > nodo.partidas[indice].id_partida:
            indice += 1

        if indice < len(nodo.partidas) and id_partida == nodo.partidas[indice].id_partida:
            return nodo.partidas[indice]

        if nodo.hoja:
            return None

        return self._buscar_recursivo(nodo.hijos[indice], id_partida)

    def mostrar_historial(self):
        """
        Muestra todas las partidas guardadas en orden.
        """
        print()
        print("===================================")
        print("        HISTORIAL DE PARTIDAS      ")
        print("===================================")

        if len(self.raiz.partidas) == 0:
            print("No hay partidas registradas.")
            return

        self._mostrar_inorden(self.raiz)

    def _mostrar_inorden(self, nodo):
        """
        Recorre el árbol B en orden.
        """

        indice = 0

        while indice < len(nodo.partidas):
            if not nodo.hoja:
                self._mostrar_inorden(nodo.hijos[indice])

            print("-----------------------------------")
            print(nodo.partidas[indice].mostrar())

            indice += 1

        if not nodo.hoja:
            self._mostrar_inorden(nodo.hijos[indice])

    def limpiar(self):
        """
        Reinicia el árbol B.
        """
        self.raiz = NodoB(True)