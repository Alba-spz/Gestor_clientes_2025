import os
import platform

def limpiar_pantalla():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    if mensaje:
        print(mensaje)

    while True:
        texto = input("> ")
        if longitud_min <= len(texto) <= longitud_max:
            return texto
        print(f"Debe tener entre {longitud_min} y {longitud_max} caracteres.")
