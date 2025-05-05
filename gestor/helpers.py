import os
import platform
import re

# Limpiar la pantalla dependiendo del sistema operativo
def limpiar_pantalla():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

# Leer texto con restricciones de longitud mínima y máxima
def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    # Mostrar un mensaje opcional si se proporciona
    if mensaje:
        print(mensaje)

    while True:
        # Solicitar entrada del usuario
        texto = input("> ")
        # Validar que la longitud del texto esté dentro del rango permitido
        if longitud_min <= len(texto) <= longitud_max:
            return texto
        # Mostrar mensaje de error si no cumple con las restricciones
        print(f"Debe tener entre {longitud_min} y {longitud_max} caracteres.")

# Validar si un DNI es válido y no está repetido en la lista de clientes
def dni_valido(dni, lista_clientes):
    # Verificar que el formato del DNI sea correcto (2 números y 1 letra mayúscula)
    if not re.match(r'^[0-9]{2}[A-Z]$', dni):
        print("❌ DNI incorrecto: debe tener el formato '99X'")
        return False

    # Comprobar si el DNI ya está siendo usado por otro cliente
    for cliente in lista_clientes:
        if cliente.dni == dni:
            print("❌ Ese DNI ya está siendo usado por otro cliente.")
            return False

    return True

# Validar si un nombre es válido (solo letras y longitud entre 2 y 30)
def nombre_valido(nombre):
    return nombre.isalpha() and 2 <= len(nombre) <= 30

# Validar si un apellido es válido (solo letras y longitud entre 2 y 30)
def apellido_valido(apellido):
    return apellido.isalpha() and 2 <= len(apellido) <= 30
