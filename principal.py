from clientes import Cliente
from empresa import Empresa

if __name__ == "__main__":
    hector = Cliente(nombre="Hector", apellidos="Costa Guzman", dni="11111111A")
    juan = Cliente("22222222B", "Juan", "Gonzalez Marquez")
    # Creo una empresa con los clientes iniciales
    empresa = Empresa(clientes=[hector, juan])
    # Muestro todos los clientes
    print("==LISTADO DE CLIENTES==")
    print(empresa.clientes)
    print("\n==MOSTRAR CLIENTES POR DNI==")
    # Consulto clientes por DNI
    empresa.mostrar_cliente("11111111A")
    empresa.mostrar_cliente("11111111Z")
    print("\n==BORRAR CLIENTES POR DNI==")
    # Borro un cliente por DNI
    empresa.borrar_cliente("22222222V")
    empresa.borrar_cliente("22222222B")
    # Muestro de nuevo todos los clientes
    print("\n==LISTADO DE CLIENTES==")
    print(empresa.clientes)
    # Añañdo un nuevo cliente
    print("\n==AÑADIR NUEVO CLIENTE==")
    empresa.añadir_cliente(Cliente("33333333C", "Lara", "Perez"))
    # Muestro de nuevo todos los clientes
    print("\n==LISTADO DE CLIENTES==")
    print(empresa.clientes)