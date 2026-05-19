# main.py

from src.interfaz.ventana_principal import VentanaPrincipal


def main():
    """
    Punto de entrada principal del programa.
    """

    app = VentanaPrincipal()
    app.iniciar()


if __name__ == "__main__":
    main()