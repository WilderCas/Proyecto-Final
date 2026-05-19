import random
import os

from src.juego.tablero import Tablero
from src.juego.jugador import Jugador
from src.estructuras.lista_enlazada import ListaEnlazada
from src.estructuras.arbol_avl import ArbolAVL
from src.aprendizaje.aprendizaje import Aprendizaje
from src.historial.historial_partidas import HistorialPartidas
from src.utilidades.graphviz_manager import GraphvizManager


class JuegoTotito:
    """
    Clase principal que controla una partida de Totito.

    Se encarga de:
    - Crear el tablero.
    - Controlar los turnos.
    - Validar ganador.
    - Detectar empate.
    - Guardar las jugadas realizadas.
    - Usar un árbol AVL para elegir movimientos del programa.
    - Aplicar aprendizaje mediante pesos.
    """

    def __init__(self, grado_arbol_b=2):
        self.tablero = Tablero()

        self.jugador_humano = Jugador("Jugador Humano", "X", "HUMANO")
        self.jugador_programa = Jugador("Programa", "O", "PROGRAMA")

        self.turno_actual = self.jugador_humano

        self.jugadas_realizadas = ListaEnlazada()
        self.jugadas_programa = ListaEnlazada()

        self.arbol_movimientos = ArbolAVL()
        self.arbol_movimientos.cargar_movimientos_iniciales()

        self.aprendizaje = Aprendizaje(self.arbol_movimientos)

        self.grado_arbol_b = grado_arbol_b
        self.historial = HistorialPartidas(grado_arbol_b=self.grado_arbol_b)

        self.graphviz_manager = GraphvizManager()

        self.partidas_jugadas = 0

    def configurar_grado_arbol_b(self, nuevo_grado):
        """
        Configura el grado mínimo del Árbol B.

        Importante:
        Al cambiar el grado, se reinicia el historial porque el Árbol B
        debe reconstruirse con la nueva configuración.
        """

        if nuevo_grado < 2:
            return False

        self.grado_arbol_b = nuevo_grado
        self.historial = HistorialPartidas(grado_arbol_b=self.grado_arbol_b)

        self.partidas_jugadas = 0

        self.limpiar_imagenes_graphviz()

        return True


    def limpiar_imagenes_graphviz(self):
        """
        Elimina todos los archivos generados por Graphviz.

        Borra archivos .png y .dot dentro de la carpeta imagenes_graphviz.
        Esto sirve cuando se cambia el grado del Árbol B o se reinicia el proyecto.
        """

        carpeta = "imagenes_graphviz"

        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
            return

        for nombre_archivo in os.listdir(carpeta):
            ruta_archivo = os.path.join(carpeta, nombre_archivo)

            if os.path.isfile(ruta_archivo):
                if nombre_archivo.endswith(".png") or nombre_archivo.endswith(".dot"):
                    os.remove(ruta_archivo)

    def reiniciar_partida(self):
        """
        Reinicia únicamente el tablero y las jugadas de la partida actual.
        No borra el aprendizaje.
        """
        self.tablero.reiniciar()
        self.jugadas_realizadas.limpiar()
        self.jugadas_programa.limpiar()
        self.turno_actual = self.jugador_humano

    def reiniciar_aprendizaje(self):
        """
        Reinicia el árbol AVL, el historial y las estadísticas del aprendizaje.
        """
        self.arbol_movimientos.reiniciar()
        self.aprendizaje = Aprendizaje(self.arbol_movimientos)
        self.historial.limpiar()
        self.partidas_jugadas = 0
        self.limpiar_imagenes_graphviz()

    def cambiar_turno(self):
        """
        Cambia el turno entre jugador humano y programa.
        """
        if self.turno_actual == self.jugador_humano:
            self.turno_actual = self.jugador_programa
        else:
            self.turno_actual = self.jugador_humano

    def registrar_jugada(self, jugador, posicion):
        """
        Guarda una jugada dentro de la lista enlazada.
        """
        texto_jugada = f"{jugador.nombre} colocó {jugador.simbolo} en posición {posicion}"
        self.jugadas_realizadas.agregar_final(texto_jugada)

        if jugador.tipo == "PROGRAMA":
            self.jugadas_programa.agregar_final(posicion)

    def realizar_jugada(self, posicion):
        """
        Intenta realizar una jugada en el tablero.
        """
        simbolo = self.turno_actual.simbolo

        pudo_colocar = self.tablero.colocar_simbolo(posicion, simbolo)

        if pudo_colocar:
            self.registrar_jugada(self.turno_actual, posicion)
            return True

        return False

    def tres_casillas_iguales(self, posicion_a, posicion_b, posicion_c):
        """
        Verifica si tres casillas tienen el mismo símbolo.

        Esto evita usar arreglos o matrices para validar ganador.
        """
        valor_a = self.tablero.obtener_casilla(posicion_a)
        valor_b = self.tablero.obtener_casilla(posicion_b)
        valor_c = self.tablero.obtener_casilla(posicion_c)

        if valor_a != " " and valor_a == valor_b and valor_b == valor_c:
            return valor_a

        return None

    def verificar_ganador(self):
        """
        Verifica todas las combinaciones posibles de victoria.
        """

        ganador = self.tres_casillas_iguales(0, 1, 2)
        if ganador is not None:
            return ganador

        ganador = self.tres_casillas_iguales(3, 4, 5)
        if ganador is not None:
            return ganador

        ganador = self.tres_casillas_iguales(6, 7, 8)
        if ganador is not None:
            return ganador

        ganador = self.tres_casillas_iguales(0, 3, 6)
        if ganador is not None:
            return ganador

        ganador = self.tres_casillas_iguales(1, 4, 7)
        if ganador is not None:
            return ganador

        ganador = self.tres_casillas_iguales(2, 5, 8)
        if ganador is not None:
            return ganador

        ganador = self.tres_casillas_iguales(0, 4, 8)
        if ganador is not None:
            return ganador

        ganador = self.tres_casillas_iguales(2, 4, 6)
        if ganador is not None:
            return ganador

        return None

    def obtener_nombre_ganador(self, simbolo_ganador):
        """
        Convierte el símbolo ganador en el nombre del jugador.
        """
        if simbolo_ganador == self.jugador_humano.simbolo:
            return self.jugador_humano.nombre

        if simbolo_ganador == self.jugador_programa.simbolo:
            return self.jugador_programa.nombre

        return "Sin ganador"

    def obtener_resultado_aprendizaje(self, simbolo_ganador):
        """
        Convierte el símbolo ganador en un resultado entendible
        para la clase Aprendizaje.
        """
        if simbolo_ganador == self.jugador_programa.simbolo:
            return "PROGRAMA"

        if simbolo_ganador == self.jugador_humano.simbolo:
            return "HUMANO"

        return "EMPATE"

    def mostrar_jugadas(self):
        """
        Muestra las jugadas realizadas en la partida.
        """
        print()
        print("Jugadas realizadas:")
        self.jugadas_realizadas.mostrar()

    def elegir_jugada_programa(self):
        """
        El programa elige una jugada usando aprendizaje progresivo.

        La dificultad aumenta según la cantidad de iteraciones aprendidas.
        Al inicio juega más simple.
        Con más partidas, bloquea mejor, usa más estrategia y aprovecha
        los pesos del Árbol AVL.
        """

        iteraciones = self.aprendizaje.iteraciones

        # Configuración progresiva de dificultad.
        # Mientras más iteraciones existan, mejor juega el programa.
        if iteraciones < 10:
            probabilidad_bloqueo = 35
            probabilidad_centro = 40
            probabilidad_esquina = 35
            probabilidad_explorar = 45

        elif iteraciones < 40:
            probabilidad_bloqueo = 55
            probabilidad_centro = 55
            probabilidad_esquina = 50
            probabilidad_explorar = 30

        elif iteraciones < 100:
            probabilidad_bloqueo = 75
            probabilidad_centro = 70
            probabilidad_esquina = 65
            probabilidad_explorar = 20

        else:
            probabilidad_bloqueo = 85
            probabilidad_centro = 80
            probabilidad_esquina = 75
            probabilidad_explorar = 12

        # 1. Si el programa puede ganar, no siempre gana al inicio.
        # Esto permite que la primera etapa no sea perfecta.
        jugada_ganadora = self.buscar_jugada_ganadora(self.jugador_programa.simbolo)

        if jugada_ganadora is not None:
            probabilidad_ganar = 60

            if iteraciones >= 10:
                probabilidad_ganar = 75

            if iteraciones >= 40:
                probabilidad_ganar = 90

            if iteraciones >= 100:
                probabilidad_ganar = 95

            numero = random.randint(1, 100)

            if numero <= probabilidad_ganar:
                return jugada_ganadora

        # 2. Si el humano puede ganar, el programa intenta bloquear.
        # Al inicio bloquea poco, luego mejora.
        jugada_bloqueo = self.buscar_jugada_ganadora(self.jugador_humano.simbolo)

        if jugada_bloqueo is not None:
            numero = random.randint(1, 100)

            if numero <= probabilidad_bloqueo:
                return jugada_bloqueo

        # 3. Exploración: al inicio explora mucho.
        # Con más aprendizaje, explora menos.
        numero_explorar = random.randint(1, 100)

        if numero_explorar <= probabilidad_explorar:
            return self.elegir_jugada_aleatoria()

        # 4. Tomar el centro según nivel de aprendizaje.
        if self.tablero.posicion_disponible(4):
            numero_centro = random.randint(1, 100)

            if numero_centro <= probabilidad_centro:
                return 4

        # 5. Tomar una esquina según nivel de aprendizaje.
        esquina = self.buscar_esquina_disponible()

        if esquina is not None:
            numero_esquina = random.randint(1, 100)

            if numero_esquina <= probabilidad_esquina:
                return esquina

        # 6. Usar el Árbol AVL con pesos aprendidos.
        jugada_avl = self.arbol_movimientos.elegir_mejor_movimiento_disponible(self.tablero)

        if jugada_avl is not None:
            return jugada_avl

        # 7. Último recurso.
        return self.elegir_jugada_aleatoria()
    
    def buscar_jugada_ganadora(self, simbolo):
        """
        Busca si existe una jugada que permita ganar inmediatamente.

        También sirve para bloquear, porque si revisamos con el símbolo
        del humano, encontramos dónde el humano podría ganar.
        """

        posicion = 0

        while posicion < 9:
            if self.tablero.posicion_disponible(posicion):

                # Colocamos temporalmente el símbolo.
                self.tablero.casillas.modificar_por_indice(posicion, simbolo)

                ganador = self.verificar_ganador()

                # Quitamos el símbolo temporal.
                self.tablero.casillas.modificar_por_indice(posicion, " ")

                if ganador == simbolo:
                    return posicion

            posicion += 1

        return None

    def buscar_esquina_disponible(self):
        """
        Busca una esquina disponible.

        Esquinas:
        0, 2, 6, 8
        """

        if self.tablero.posicion_disponible(0):
            return 0

        if self.tablero.posicion_disponible(2):
            return 2

        if self.tablero.posicion_disponible(6):
            return 6

        if self.tablero.posicion_disponible(8):
            return 8

        return None

    def buscar_esquina_disponible(self):
        """
        Busca una esquina disponible.

        Esquinas del tablero:
        0 | 2
        -----
        6 | 8
        """

        if self.tablero.posicion_disponible(0):
            return 0

        if self.tablero.posicion_disponible(2):
            return 2

        if self.tablero.posicion_disponible(6):
            return 6

        if self.tablero.posicion_disponible(8):
            return 8

        return None
    
    def contar_posiciones_disponibles(self):
        """
        Cuenta cuántas posiciones libres tiene el tablero.

        No usamos listas para guardar las posiciones disponibles,
        solo contamos recorriendo de 0 a 8.
        """
        contador = 0
        posicion = 0

        while posicion < 9:
            if self.tablero.posicion_disponible(posicion):
                contador += 1

            posicion += 1

        return contador

    def elegir_jugada_aleatoria(self):
        """
        Elige una posición libre aleatoria.

        Esta función simula al jugador humano durante
        el entrenamiento automático.
        """
        cantidad_disponibles = self.contar_posiciones_disponibles()

        if cantidad_disponibles == 0:
            return None

        numero_elegido = random.randint(1, cantidad_disponibles)

        contador = 0
        posicion = 0

        while posicion < 9:
            if self.tablero.posicion_disponible(posicion):
                contador += 1

                if contador == numero_elegido:
                    return posicion

            posicion += 1

        return None

    def simular_partida_automatica(self):
        """
        Simula una partida completa.

        En esta simulación:
        - El programa usa el árbol AVL y sus pesos.
        - El jugador humano simulado juega aleatoriamente.

        Retorna:
        - resultado final de la partida.
        - id de la partida guardada.
        """

        self.reiniciar_partida()

        partida_activa = True
        resultado_final = "EMPATE"
        simbolo_ganador = None

        while partida_activa:

            if self.turno_actual.tipo == "HUMANO":
                posicion = self.elegir_jugada_aleatoria()
            else:
                posicion = self.elegir_jugada_programa()

            if posicion is None:
                resultado_final = "EMPATE"
                partida_activa = False
                continue

            jugada_correcta = self.realizar_jugada(posicion)

            if not jugada_correcta:
                # Si por alguna razón eligió una posición inválida,
                # se busca otra jugada aleatoria.
                posicion = self.elegir_jugada_aleatoria()
                self.realizar_jugada(posicion)

            ganador = self.verificar_ganador()

            if ganador is not None:
                simbolo_ganador = ganador
                resultado_final = self.obtener_resultado_aprendizaje(ganador)
                partida_activa = False

            elif self.tablero.tablero_lleno():
                resultado_final = "EMPATE"
                partida_activa = False

            else:
                self.cambiar_turno()

        id_partida = self.finalizar_partida_automatica(resultado_final, simbolo_ganador)

        return resultado_final, id_partida

    def finalizar_partida_automatica(self, resultado, simbolo_ganador=None):
        """
        Finaliza una partida automática sin mostrar tanto detalle en pantalla.

        Aplica aprendizaje, guarda la partida en el historial
        y genera visualizaciones.
        """
        self.partidas_jugadas += 1

        self.aprendizaje.aprender_de_partida(resultado, self.jugadas_programa)

        tablero_final = self.tablero.obtener_estado_como_texto()

        id_partida = self.historial.registrar_partida(
            resultado,
            tablero_final,
            self.jugadas_realizadas
        )

        self.generar_visualizaciones_partida(id_partida)

        return id_partida
    
    def generar_visualizaciones_partida(self, id_partida):
        """
        Genera las visualizaciones de las estructuras usadas.

        Se generan:
        - Árbol AVL de movimientos con pesos.
        - Árbol B del historial de partidas.
        """

        ruta_avl_dot, ruta_avl_png = self.graphviz_manager.generar_visualizacion_avl(
            self.arbol_movimientos,
            id_partida
        )

        ruta_b_dot, ruta_b_png = self.graphviz_manager.generar_visualizacion_arbol_b(
            self.historial.arbol_b,
            id_partida
        )

        print()
        print("Visualizaciones generadas:")

        print(f"AVL DOT: {ruta_avl_dot}")

        if ruta_avl_png is not None:
            print(f"AVL PNG: {ruta_avl_png}")

        print(f"Árbol B DOT: {ruta_b_dot}")

        if ruta_b_png is not None:
            print(f"Árbol B PNG: {ruta_b_png}")

    def entrenamiento_automatico(self, cantidad_partidas):
        """
        Ejecuta varias partidas automáticas.

        Genera un reporte en la carpeta reportes.
        """

        if cantidad_partidas <= 0:
            print("La cantidad de partidas debe ser mayor que 0.")
            return

        print()
        print("===================================")
        print("       ENTRENAMIENTO AUTOMÁTICO    ")
        print("===================================")
        print(f"Partidas a simular: {cantidad_partidas}")
        print("Entrenando...")

        reporte = ""
        reporte += "REPORTE DE ENTRENAMIENTO AUTOMÁTICO\n"
        reporte += "===================================\n"
        reporte += f"Cantidad de partidas simuladas: {cantidad_partidas}\n\n"
        reporte += "Listado de partidas simuladas:\n"

        contador = 1

        while contador <= cantidad_partidas:
            resultado, id_partida = self.simular_partida_automatica()

            reporte += f"Simulación {contador} | ID Partida: {id_partida} | Resultado: {resultado}\n"

            contador += 1

        reporte += "\n"
        reporte += "Estado final de aprendizaje:\n"
        reporte += self.aprendizaje.obtener_texto_estadisticas()
        reporte += "\n"
        reporte += "Pesos finales del Árbol AVL:\n"
        reporte += self.obtener_pesos_avl_como_texto()

        self.guardar_reporte_entrenamiento(reporte)

        print("Entrenamiento finalizado correctamente.")
        print()
        self.aprendizaje.mostrar_estadisticas()
        print("Reporte generado en la carpeta reportes.")

    def obtener_pesos_avl_como_texto(self):
        """
        Retorna los pesos del árbol AVL como texto.

        Esto se usa para el reporte de entrenamiento.
        """
        texto = ""
        texto = self._obtener_pesos_avl_recursivo(self.arbol_movimientos.raiz, texto)
        return texto

    def _obtener_pesos_avl_recursivo(self, nodo_actual, texto):
        """
        Recorre el árbol AVL en inorden para obtener sus pesos.
        """
        if nodo_actual is not None:
            texto = self._obtener_pesos_avl_recursivo(nodo_actual.izquierda, texto)

            movimiento = nodo_actual.movimiento
            texto += f"Posición: {movimiento.posicion} | Peso: {movimiento.peso}\n"

            texto = self._obtener_pesos_avl_recursivo(nodo_actual.derecha, texto)

        return texto

    def guardar_reporte_entrenamiento(self, contenido):
        """
        Guarda el reporte del entrenamiento automático en un archivo txt.
        """
        carpeta_reportes = "reportes"

        if not os.path.exists(carpeta_reportes):
            os.makedirs(carpeta_reportes)

        nombre_archivo = f"reporte_entrenamiento_{self.aprendizaje.iteraciones}.txt"
        ruta = os.path.join(carpeta_reportes, nombre_archivo)

        archivo = open(ruta, "w", encoding="utf-8")
        archivo.write(contenido)
        archivo.close()

    def finalizar_partida(self, resultado, simbolo_ganador=None):
        """
        Finaliza una partida, aplica aprendizaje, guarda historial
        y muestra resumen.
        """
        self.partidas_jugadas += 1

        self.aprendizaje.aprender_de_partida(resultado, self.jugadas_programa)

        tablero_final = self.tablero.obtener_estado_como_texto()

        id_partida = self.historial.registrar_partida(
            resultado,
            tablero_final,
            self.jugadas_realizadas
        )

        self.generar_visualizaciones_partida(id_partida)

        print()
        print("===================================")
        print("          FIN DE LA PARTIDA        ")
        print("===================================")

        if resultado == "EMPATE":
            print("Resultado: Empate")
        else:
            nombre_ganador = self.obtener_nombre_ganador(simbolo_ganador)
            print(f"Ganador: {nombre_ganador}")

        print(f"ID de partida guardada: {id_partida}")
        print(f"Partidas jugadas: {self.partidas_jugadas}")
        print(f"Tablero final guardado: {tablero_final}")

        self.mostrar_jugadas()

        print()
        self.arbol_movimientos.mostrar_inorden()

    def procesar_jugada_humano_interfaz(self, posicion):
            """
            Procesa una jugada realizada desde la interfaz gráfica.

            Flujo:
            1. El humano coloca X.
            2. Se verifica si ganó o empató.
            3. Si la partida sigue, juega el programa.
            4. Se vuelve a verificar ganador o empate.

            Retorna un texto indicando el estado de la partida:
            - "CONTINUA"
            - "HUMANO"
            - "PROGRAMA"
            - "EMPATE"
            - "INVALIDA"
            """

            if self.turno_actual.tipo != "HUMANO":
                return "INVALIDA"

            jugada_correcta = self.realizar_jugada(posicion)

            if not jugada_correcta:
                return "INVALIDA"

            ganador = self.verificar_ganador()

            if ganador is not None:
                resultado = self.obtener_resultado_aprendizaje(ganador)
                self.finalizar_partida(resultado, ganador)
                return resultado

            if self.tablero.tablero_lleno():
                self.finalizar_partida("EMPATE")
                return "EMPATE"

            self.cambiar_turno()

            resultado_programa = self.procesar_jugada_programa_interfaz()

            return resultado_programa

    def procesar_jugada_programa_interfaz(self):
        """
        Procesa la jugada del programa desde la interfaz gráfica.

        El programa usa el Árbol AVL para elegir la mejor posición disponible.
        """

        if self.turno_actual.tipo != "PROGRAMA":
            return "INVALIDA"

        posicion = self.elegir_jugada_programa()

        if posicion is None:
            self.finalizar_partida("EMPATE")
            return "EMPATE"

        jugada_correcta = self.realizar_jugada(posicion)

        if not jugada_correcta:
            return "INVALIDA"

        ganador = self.verificar_ganador()

        if ganador is not None:
            resultado = self.obtener_resultado_aprendizaje(ganador)
            self.finalizar_partida(resultado, ganador)
            return resultado

        if self.tablero.tablero_lleno():
            self.finalizar_partida("EMPATE")
            return "EMPATE"

        self.cambiar_turno()

        return "CONTINUA"

    def jugar_consola(self):
        """
        Ejecuta una partida completa desde consola.
        """
        self.reiniciar_partida()

        print("===================================")
        print("       NUEVA PARTIDA DE TOTITO      ")
        print("===================================")
        print("Tú eres X y el programa es O.")
        print("Selecciona posiciones del 0 al 8.")
        print()

        partida_activa = True

        while partida_activa:
            self.tablero.mostrar_tablero()

            if self.turno_actual.tipo == "HUMANO":
                try:
                    posicion = int(input("Ingresa una posición del 0 al 8: "))
                except ValueError:
                    print("Error: debes ingresar un número.")
                    continue
            else:
                posicion = self.elegir_jugada_programa()
                print(f"El programa eligió la posición {posicion}")

            jugada_correcta = self.realizar_jugada(posicion)

            if not jugada_correcta:
                print("Movimiento inválido. Intenta de nuevo.")
                continue

            ganador = self.verificar_ganador()

            if ganador is not None:
                self.tablero.mostrar_tablero()
                resultado = self.obtener_resultado_aprendizaje(ganador)
                self.finalizar_partida(resultado, ganador)
                partida_activa = False

            elif self.tablero.tablero_lleno():
                self.tablero.mostrar_tablero()
                self.finalizar_partida("EMPATE")
                partida_activa = False

            else:
                self.cambiar_turno()