import csv
import config
import os

# Define la clase Cliente para representar a un cliente
class Cliente:
    def __init__(self, dni, nombre, apellido):
        # Inicializar los atributos del cliente
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        # Devolver una representación en cadena del cliente
        return f"({self.dni}) {self.nombre} {self.apellido}"
    
# Define la clase Clientes para gestionar una lista de clientes
class Clientes:
    # Inicializar la lista de clientes
    lista = []

    # Asegurar que el archivo de base de datos existe antes de intentar leerlo
    if not os.path.exists(config.DATABASE_PATH):
        with open(config.DATABASE_PATH, "w", newline="\n") as fichero:
            pass  # Crear un archivo vacío si no existe
    
    # Leer los datos del archivo de base de datos y cargar los clientes en la lista
    with open(config.DATABASE_PATH, newline="\n") as fichero:
        reader = csv.reader(fichero, delimiter=";")
        for fila in reader:
            if len(fila) == 3:  # Verificar que la fila tiene exactamente 3 elementos
                dni, nombre, apellido = fila
                cliente = Cliente(dni, nombre, apellido)
                lista.append(cliente)

    # Buscar un cliente por su DNI
    @staticmethod
    def buscar(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente
    
    # Crear un nuevo cliente y guardarlo en la lista
    @staticmethod
    def crear(dni, nombre, apellido):
        cliente = Cliente(dni, nombre, apellido)
        Clientes.lista.append(cliente)
        Clientes.guardar()  # Guardar los cambios en el archivo
        return cliente
    
    # Modificar los datos de un cliente existente
    @staticmethod
    def modificar(dni, nombre, apellido):
        for i, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                # Actualizar los datos del cliente
                Clientes.lista[i].nombre = nombre
                Clientes.lista[i].apellido = apellido
                Clientes.guardar()  # Guardar los cambios en el archivo
                return Clientes.lista[i]
            
    # Borrar un cliente de la lista
    @staticmethod
    def borrar(dni):
        for i, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                # Eliminar el cliente de la lista
                cliente = Clientes.lista.pop(i)
                Clientes.guardar()  # Guardar los cambios en el archivo
                return cliente
            
    # Guardar la lista de clientes en el archivo de base de datos
    @staticmethod
    def guardar():
        with open(config.DATABASE_PATH, "w", newline="\n") as fichero:
            writer = csv.writer(fichero, delimiter=";")
            for c in Clientes.lista:
                # Escribir los datos de cada cliente en el archivo
                writer.writerow((c.dni, c.nombre, c.apellido))