import sys
import menu
import ui

if __name__ == "__main__":
    # Comprueba si se pasa un argumento -t para lanzar el modo terminal
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        # Inicia el modo terminal
        menu.iniciar()
    # Lanza el modo gráfico en cualquier otro caso
    else:
        # Crea una instancia de la ventana principal de la interfaz gráfica
        app = ui.MainWindow()
        # Ejecuta el bucle principal de la aplicación gráfica
        app.mainloop()

