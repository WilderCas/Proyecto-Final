class Nodo:
    """
    Nodo básico para una lista enlazada simple.

    Cada nodo guarda:
    - dato: la información que queremos almacenar.
    - siguiente: referencia al siguiente nodo.
    """

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    """
    Lista enlazada simple creada manualmente.

    La usaremos para evitar depender de listas normales de Python
    como estructura principal del proyecto.
    """

    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def esta_vacia(self):
        """
        Retorna True si la lista no tiene nodos.
        """
        return self.cabeza is None

    def agregar_final(self, dato):
        """
        Agrega un nuevo dato al final de la lista.
        """
        nuevo_nodo = Nodo(dato)

        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza

            while actual.siguiente is not None:
                actual = actual.siguiente

            actual.siguiente = nuevo_nodo

        self.tamano += 1

    def obtener_por_indice(self, indice):
        """
        Obtiene un dato según su posición dentro de la lista.

        Ejemplo:
        indice 0 = primer nodo
        indice 1 = segundo nodo
        """
        if indice < 0 or indice >= self.tamano:
            return None

        actual = self.cabeza
        contador = 0

        while actual is not None:
            if contador == indice:
                return actual.dato

            actual = actual.siguiente
            contador += 1

        return None

    def modificar_por_indice(self, indice, nuevo_dato):
        """
        Cambia el dato de un nodo según su posición.
        """
        if indice < 0 or indice >= self.tamano:
            return False

        actual = self.cabeza
        contador = 0

        while actual is not None:
            if contador == indice:
                actual.dato = nuevo_dato
                return True

            actual = actual.siguiente
            contador += 1

        return False

    def mostrar(self):
        """
        Muestra todos los datos de la lista.
        """
        actual = self.cabeza

        while actual is not None:
            print(actual.dato)
            actual = actual.siguiente

    def limpiar(self):
        """
        Vacía la lista.
        """
        self.cabeza = None
        self.tamano = 0