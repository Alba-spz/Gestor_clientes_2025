import os
import platform
import re

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

def dni_valido(dni, lista_clientes):
    # Debe tener exactamente 2 números y 1 letra mayúscula al final
    if not re.match(r'^[0-9]{2}[A-Z]$', dni):
        print("❌ DNI incorrecto: debe tener el formato '99X'")
        return False

    # Comprobar si ya existe un cliente con ese DNI
    for cliente in lista_clientes:
        if cliente.dni == dni:
            print("❌ Ese DNI ya está siendo usado por otro cliente.")
            return False

    return True
