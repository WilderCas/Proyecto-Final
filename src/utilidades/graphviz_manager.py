import os
import subprocess
import shutil


class GraphvizManager:
    """
    Clase encargada de generar archivos Graphviz.

    Genera:
    - Archivo .dot
    - Archivo .png si Graphviz está instalado en la computadora

    No usamos librería externa de Python.
    Creamos el texto DOT manualmente.
    """

    def __init__(self, carpeta_salida="imagenes_graphviz"):
        self.carpeta_salida = carpeta_salida
        self.crear_carpeta_si_no_existe()

    def crear_carpeta_si_no_existe(self):
        """
        Crea la carpeta donde se guardarán las imágenes.
        """
        if not os.path.exists(self.carpeta_salida):
            os.makedirs(self.carpeta_salida)

    def guardar_archivo_dot(self, nombre_archivo, contenido):
        """
        Guarda un archivo .dot.
        """
        ruta_dot = os.path.join(self.carpeta_salida, nombre_archivo + ".dot")

        archivo = open(ruta_dot, "w", encoding="utf-8")
        archivo.write(contenido)
        archivo.close()

        return ruta_dot

    def convertir_dot_a_png(self, ruta_dot):
        """
        Convierte un archivo .dot a .png usando Graphviz.

        Para que funcione, Graphviz debe estar instalado
        y el comando dot debe estar disponible.
        """

        if shutil.which("dot") is None:
            print("Aviso: Graphviz no está instalado o el comando dot no está disponible.")
            print("Se generó el archivo .dot, pero no se pudo generar la imagen .png.")
            return None

        ruta_png = ruta_dot.replace(".dot", ".png")

        comando = ["dot", "-Tpng", ruta_dot, "-o", ruta_png]

        try:
            subprocess.run(comando, check=True)
            return ruta_png
        except Exception as error:
            print("Error al generar imagen PNG con Graphviz:")
            print(error)
            return None

    def generar_visualizacion_avl(self, arbol_avl, id_partida):
        """
        Genera la visualización del Árbol AVL.

        Este árbol muestra:
        - Posición del movimiento
        - Peso actual del movimiento
        """

        contenido = ""
        contenido += "digraph AVL {\n"
        contenido += "    graph [label=\"Árbol AVL de Movimientos - Partida " + str(id_partida) + "\", labelloc=t, fontsize=20];\n"
        contenido += "    node [shape=record, style=filled, fillcolor=lightblue];\n"
        contenido += "    edge [color=black];\n\n"

        if arbol_avl.raiz is None:
            contenido += "    vacio [label=\"Árbol vacío\"];\n"
        else:
            contenido += self._generar_nodos_avl(arbol_avl.raiz)

        contenido += "}\n"

        nombre_archivo = "partida_" + str(id_partida) + "_arbol_avl"
        ruta_dot = self.guardar_archivo_dot(nombre_archivo, contenido)
        ruta_png = self.convertir_dot_a_png(ruta_dot)

        return ruta_dot, ruta_png

    def _generar_nodos_avl(self, nodo):
        """
        Genera recursivamente los nodos y conexiones del Árbol AVL.
        """

        if nodo is None:
            return ""

        contenido = ""

        movimiento = nodo.movimiento

        nombre_nodo = "nodo_" + str(movimiento.posicion)

        etiqueta = "Posición: " + str(movimiento.posicion)
        etiqueta += "\\nPeso: " + str(movimiento.peso)
        etiqueta += "\\nAltura: " + str(nodo.altura)

        contenido += "    " + nombre_nodo + " [label=\"" + etiqueta + "\"];\n"

        if nodo.izquierda is not None:
            nombre_izquierdo = "nodo_" + str(nodo.izquierda.movimiento.posicion)
            contenido += "    " + nombre_nodo + " -> " + nombre_izquierdo + " [label=\"Izq\"];\n"
            contenido += self._generar_nodos_avl(nodo.izquierda)

        if nodo.derecha is not None:
            nombre_derecho = "nodo_" + str(nodo.derecha.movimiento.posicion)
            contenido += "    " + nombre_nodo + " -> " + nombre_derecho + " [label=\"Der\"];\n"
            contenido += self._generar_nodos_avl(nodo.derecha)

        return contenido

    def generar_visualizacion_arbol_b(self, arbol_b, id_partida):
        """
        Genera la visualización del Árbol B del historial.

        Este árbol muestra:
        - IDs de partidas
        - Resultado de cada partida
        """

        contenido = ""
        contenido += "digraph ArbolB {\n"
        contenido += "    graph [label=\"Árbol B Historial de Partidas - Partida " + str(id_partida) + "\", labelloc=t, fontsize=20];\n"
        contenido += "    node [shape=record, style=filled, fillcolor=lightyellow];\n"
        contenido += "    edge [color=black];\n\n"

        if arbol_b.raiz is None or len(arbol_b.raiz.partidas) == 0:
            contenido += "    vacio [label=\"Historial vacío\"];\n"
        else:
            contenido += self._generar_nodos_b(arbol_b.raiz, "raiz")

        contenido += "}\n"

        nombre_archivo = "partida_" + str(id_partida) + "_arbol_b_historial"
        ruta_dot = self.guardar_archivo_dot(nombre_archivo, contenido)
        ruta_png = self.convertir_dot_a_png(ruta_dot)

        return ruta_dot, ruta_png

    def _generar_nodos_b(self, nodo, nombre_nodo):
        """
        Genera recursivamente los nodos y conexiones del Árbol B.
        """

        contenido = ""

        etiqueta = ""

        indice = 0

        while indice < len(nodo.partidas):
            partida = nodo.partidas[indice]

            if indice > 0:
                etiqueta += "|"

            etiqueta += "ID: " + str(partida.id_partida)
            etiqueta += "\\nResultado: " + partida.resultado

            indice += 1

        contenido += "    " + nombre_nodo + " [label=\"" + etiqueta + "\"];\n"

        if not nodo.hoja:
            indice_hijo = 0

            while indice_hijo < len(nodo.hijos):
                nombre_hijo = nombre_nodo + "_hijo_" + str(indice_hijo)

                contenido += self._generar_nodos_b(nodo.hijos[indice_hijo], nombre_hijo)
                contenido += "    " + nombre_nodo + " -> " + nombre_hijo + ";\n"

                indice_hijo += 1

        return contenido