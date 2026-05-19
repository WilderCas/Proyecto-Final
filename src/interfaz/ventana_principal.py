# src/interfaz/ventana_principal.py

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

from src.juego.juego_totito import JuegoTotito


class VentanaPrincipal:
    """
    Interfaz gráfica principal del juego Totito.

    Esta ventana permite:
    - Jugar manualmente contra el programa.
    - Entrenar automáticamente.
    - Ver historial.
    - Ver estadísticas.
    - Reiniciar aprendizaje.
    - Ver integrantes.
    """

    def __init__(self):
        self.juego = JuegoTotito()

        self.ventana = tk.Tk()
        self.ventana.title("Tik Tak Toe / Totito con Aprendizaje")
        self.ventana.geometry("850x750")
        self.ventana.resizable(False, False)
        self.ventana.config(bg="#1E293B")

        self.botones_tablero = None

        self.crear_interfaz()

    def configurar_grado_arbol_b(self):
        """
        Permite configurar el grado mínimo del Árbol B desde la interfaz.
        """

        nuevo_grado = simpledialog.askinteger(
            "Configurar Árbol B",
            "Ingresa el grado mínimo del Árbol B.\nDebe ser 2 o mayor:",
            minvalue=2
        )

        if nuevo_grado is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar cambio",
            "Cambiar el grado del Árbol B reiniciará el historial actual.\n"
            "¿Deseas continuar?"
        )

        if not confirmar:
            return

        correcto = self.juego.configurar_grado_arbol_b(nuevo_grado)

        if correcto:
            messagebox.showinfo(
                "Grado configurado",
                f"El Árbol B fue configurado con grado mínimo {nuevo_grado}.\n"
                f"Máximo de claves por nodo: {(2 * nuevo_grado) - 1}."
            )
        else:
            messagebox.showerror(
                "Error",
                "El grado debe ser 2 o mayor."
            )

    def crear_interfaz(self):
        """
        Crea todos los elementos visuales de la ventana.
        """

        titulo = tk.Label(
            self.ventana,
            text="TIK TAK TOE / TOTITO",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1E293B"
        )
        titulo.pack(pady=15)

        subtitulo = tk.Label(
            self.ventana,
            text="Juego con Árbol AVL, Árbol B, aprendizaje y Graphviz",
            font=("Arial", 12),
            fg="#CBD5E1",
            bg="#1E293B"
        )
        subtitulo.pack()

        self.label_estado = tk.Label(
            self.ventana,
            text="Turno actual: Jugador Humano (X)",
            font=("Arial", 14, "bold"),
            fg="#38BDF8",
            bg="#1E293B"
        )
        self.label_estado.pack(pady=10)

        self.label_partidas = tk.Label(
            self.ventana,
            text="Partidas jugadas: 0",
            font=("Arial", 11),
            fg="white",
            bg="#1E293B"
        )
        self.label_partidas.pack()

        contenedor_principal = tk.Frame(self.ventana, bg="#1E293B")
        contenedor_principal.pack(pady=20)

        self.crear_tablero(contenedor_principal)
        self.crear_panel_botones(contenedor_principal)

    def crear_tablero(self, contenedor):
        """
        Crea el tablero gráfico de 3x3 usando botones.
        """

        frame_tablero = tk.Frame(
            contenedor,
            bg="#0F172A",
            padx=10,
            pady=10
        )
        frame_tablero.grid(row=0, column=0, padx=25)

        self.botones_tablero = []

        posicion = 0

        fila = 0
        while fila < 3:
            columna = 0

            fila_botones = []

            while columna < 3:
                boton = tk.Button(
                    frame_tablero,
                    text="",
                    font=("Arial", 30, "bold"),
                    width=4,
                    height=2,
                    bg="#F8FAFC",
                    fg="#0F172A",
                    activebackground="#E0F2FE",
                    command=lambda p=posicion: self.click_casilla(p)
                )

                boton.grid(row=fila, column=columna, padx=5, pady=5)

                fila_botones.append(boton)

                posicion += 1
                columna += 1

            self.botones_tablero.append(fila_botones)
            fila += 1

    def crear_panel_botones(self, contenedor):
        """
        Crea el panel lateral de acciones.
        """

        panel = tk.Frame(
            contenedor,
            bg="#334155",
            padx=20,
            pady=20
        )
        panel.grid(row=0, column=1, padx=25, sticky="n")

        label_menu = tk.Label(
            panel,
            text="Menú del sistema",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#334155"
        )
        label_menu.pack(pady=10)

        boton_nueva = tk.Button(
            panel,
            text="Nueva partida",
            font=("Arial", 11, "bold"),
            width=25,
            bg="#0EA5E9",
            fg="white",
            command=self.nueva_partida
        )
        boton_nueva.pack(pady=5)

        boton_entrenar = tk.Button(
            panel,
            text="Entrenamiento automático",
            font=("Arial", 11, "bold"),
            width=25,
            bg="#22C55E",
            fg="white",
            command=self.entrenamiento_automatico
        )
        boton_entrenar.pack(pady=5)

        boton_historial = tk.Button(
            panel,
            text="Ver historial",
            font=("Arial", 11, "bold"),
            width=25,
            bg="#6366F1",
            fg="white",
            command=self.ver_historial
        )
        boton_historial.pack(pady=5)

        boton_buscar = tk.Button(
            panel,
            text="Buscar partida por ID",
            font=("Arial", 11, "bold"),
            width=25,
            bg="#8B5CF6",
            fg="white",
            command=self.buscar_partida
        )
        boton_buscar.pack(pady=5)

        boton_grado = tk.Button(
            panel,
            text="Configurar grado Árbol B",
            font=("Arial", 11, "bold"),
            width=25,
            bg="#A855F7",
            fg="white",
            command=self.configurar_grado_arbol_b
        )
        boton_grado.pack(pady=5)

        boton_estadisticas = tk.Button(
            panel,
            text="Ver estadísticas",
            font=("Arial", 11, "bold"),
            width=25,
            bg="#F59E0B",
            fg="white",
            command=self.ver_estadisticas
        )
        boton_estadisticas.pack(pady=5)

        boton_reiniciar = tk.Button(
            panel,
            text="Reiniciar aprendizaje",
            font=("Arial", 11, "bold"),
            width=25,
            bg="#EF4444",
            fg="white",
            command=self.reiniciar_aprendizaje
        )
        boton_reiniciar.pack(pady=5)

        boton_integrantes = tk.Button(
            panel,
            text="Integrantes",
            font=("Arial", 11, "bold"),
            width=25,
            bg="#14B8A6",
            fg="white",
            command=self.ver_integrantes
        )
        boton_integrantes.pack(pady=5)

        boton_salir = tk.Button(
            panel,
            text="Salir",
            font=("Arial", 11, "bold"),
            width=25,
            bg="#111827",
            fg="white",
            command=self.ventana.destroy
        )
        boton_salir.pack(pady=20)

    def click_casilla(self, posicion):
        """
        Evento que ocurre cuando el jugador hace clic en una casilla.
        """

        resultado = self.juego.procesar_jugada_humano_interfaz(posicion)

        if resultado == "INVALIDA":
            messagebox.showwarning(
                "Movimiento inválido",
                "Esa casilla ya está ocupada o no es tu turno."
            )
            return

        self.actualizar_tablero()

        if resultado == "CONTINUA":
            self.label_estado.config(text="Turno actual: Jugador Humano (X)")
        elif resultado == "HUMANO":
            self.bloquear_tablero()
            self.actualizar_contador_partidas()
            messagebox.showinfo("Fin de la partida", "Ganaste la partida.")
        elif resultado == "PROGRAMA":
            self.bloquear_tablero()
            self.actualizar_contador_partidas()
            messagebox.showinfo("Fin de la partida", "Ganó el programa.")
        elif resultado == "EMPATE":
            self.bloquear_tablero()
            self.actualizar_contador_partidas()
            messagebox.showinfo("Fin de la partida", "La partida terminó en empate.")

    def actualizar_tablero(self):
        """
        Actualiza los botones según el estado real del tablero.
        """

        posicion = 0

        fila = 0
        while fila < 3:
            columna = 0

            while columna < 3:
                valor = self.juego.tablero.obtener_casilla(posicion)

                boton = self.botones_tablero[fila][columna]
                boton.config(text=valor)

                if valor == "X":
                    boton.config(fg="#2563EB")
                elif valor == "O":
                    boton.config(fg="#DC2626")
                else:
                    boton.config(fg="#0F172A")

                posicion += 1
                columna += 1

            fila += 1

    def bloquear_tablero(self):
        """
        Bloquea todos los botones del tablero.
        """

        fila = 0
        while fila < 3:
            columna = 0

            while columna < 3:
                self.botones_tablero[fila][columna].config(state="disabled")
                columna += 1

            fila += 1

    def desbloquear_tablero(self):
        """
        Habilita todos los botones del tablero.
        """

        fila = 0
        while fila < 3:
            columna = 0

            while columna < 3:
                self.botones_tablero[fila][columna].config(state="normal")
                columna += 1

            fila += 1

    def nueva_partida(self):
        """
        Limpia el tablero para iniciar una nueva partida.
        No borra el aprendizaje.
        """

        self.juego.reiniciar_partida()
        self.actualizar_tablero()
        self.desbloquear_tablero()
        self.label_estado.config(text="Turno actual: Jugador Humano (X)")

    def entrenamiento_automatico(self):
        """
        Ejecuta entrenamiento automático desde la interfaz.
        """

        cantidad = simpledialog.askinteger(
            "Entrenamiento automático",
            "¿Cuántas partidas deseas simular?",
            minvalue=1
        )

        if cantidad is None:
            return

        self.juego.entrenamiento_automatico(cantidad)

        self.actualizar_contador_partidas()

        messagebox.showinfo(
            "Entrenamiento finalizado",
            f"Se simularon {cantidad} partidas correctamente.\n"
            "El reporte fue generado en la carpeta reportes."
        )

    def ver_historial(self):
        """
        Muestra el historial en una nueva ventana.
        """

        ventana_historial = tk.Toplevel(self.ventana)
        ventana_historial.title("Historial de Partidas")
        ventana_historial.geometry("650x500")
        ventana_historial.config(bg="#0F172A")

        titulo = tk.Label(
            ventana_historial,
            text="Historial de Partidas",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#0F172A"
        )
        titulo.pack(pady=10)

        caja_texto = tk.Text(
            ventana_historial,
            width=75,
            height=25,
            font=("Consolas", 10),
            bg="#F8FAFC",
            fg="#111827"
        )
        caja_texto.pack(padx=10, pady=10)

        texto_historial = self.obtener_historial_como_texto()
        caja_texto.insert("1.0", texto_historial)
        caja_texto.config(state="disabled")

        def obtener_historial_como_texto(self):
            """
            Convierte el historial del Árbol B en texto para mostrarlo en Tkinter.
            """

            texto = ""
            texto += f"Grado mínimo del Árbol B: {self.juego.grado_arbol_b}\n"
            texto += f"Máximo de claves por nodo: {(2 * self.juego.grado_arbol_b) - 1}\n"
            texto += "===================================\n\n"

            if self.juego.historial.contador_partidas == 0:
                texto += "No hay partidas registradas."
                return texto

            texto = self._recorrer_arbol_b_texto(self.juego.historial.arbol_b.raiz, texto)

            return texto

    def _recorrer_arbol_b_texto(self, nodo, texto):
        """
        Recorre el Árbol B en orden y concatena las partidas.
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

    def buscar_partida(self):
        """
        Busca una partida por ID y la muestra en pantalla.
        """

        id_partida = simpledialog.askinteger(
            "Buscar partida",
            "Ingresa el ID de la partida:",
            minvalue=1
        )

        if id_partida is None:
            return

        partida = self.juego.historial.buscar_partida(id_partida)

        if partida is None:
            messagebox.showwarning(
                "No encontrada",
                "No se encontró una partida con ese ID."
            )
        else:
            messagebox.showinfo(
                "Partida encontrada",
                partida.mostrar()
            )

    def ver_estadisticas(self):
        """
        Muestra estadísticas del aprendizaje.
        """

        estadisticas = self.juego.aprendizaje.obtener_texto_estadisticas()

        messagebox.showinfo(
            "Estadísticas de aprendizaje",
            estadisticas
        )

    def reiniciar_aprendizaje(self):
        """
        Reinicia aprendizaje, historial y tablero.
        """

        confirmar = messagebox.askyesno(
            "Confirmar reinicio",
            "¿Seguro que deseas reiniciar el aprendizaje, historial y estructuras?"
        )

        if confirmar:
            self.juego.reiniciar_aprendizaje()
            self.juego.reiniciar_partida()
            self.actualizar_tablero()
            self.desbloquear_tablero()
            self.actualizar_contador_partidas()
            self.label_estado.config(text="Turno actual: Jugador Humano (X)")

            messagebox.showinfo(
                "Reinicio completo",
                "El aprendizaje, historial y estructuras fueron reiniciados."
            )

    def ver_integrantes(self):
        """
        Muestra los integrantes del grupo.

        Aquí debes cambiar los datos por los reales.
        """

        texto = ""
        texto += "INTEGRANTES DEL GRUPO\n"
        texto += "===================================\n"
        texto += "1. Nombre Integrante 1\n"
        texto += "   Carnet: XXXXX\n"
        texto += "   Participación: 25%\n\n"
        texto += "2. Nombre Integrante 2\n"
        texto += "   Carnet: XXXXX\n"
        texto += "   Participación: 25%\n\n"
        texto += "3. Nombre Integrante 3\n"
        texto += "   Carnet: XXXXX\n"
        texto += "   Participación: 25%\n\n"
        texto += "4. Nombre Integrante 4\n"
        texto += "   Carnet: XXXXX\n"
        texto += "   Participación: 25%\n"

        messagebox.showinfo("Integrantes", texto)

    def actualizar_contador_partidas(self):
        """
        Actualiza el contador visible de partidas jugadas.
        """

        self.label_partidas.config(
            text=f"Partidas jugadas: {self.juego.partidas_jugadas}"
        )

    def iniciar(self):
        """
        Inicia la ventana principal.
        """

        self.ventana.mainloop()