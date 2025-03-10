from clientes import Cliente
class Empresa:
    def __init__(self, clientes=None):
        if clientes is None:
            clientes = []
        self.clientes = clientes

    def mostrar_cliente(self, dni):
        for cliente in self.clientes:
            if cliente.dni == dni:
                print(cliente)
                return
        print(f"Cliente con DNI {dni} no encontrado.")

    def borrar_cliente(self, dni):
        for cliente in self.clientes:
            if cliente.dni == dni:
                self.clientes.remove(cliente)
                print(f"Cliente con DNI {dni} borrado.")
                return
        print(f"Cliente con DNI {dni} no encontrado.")

    def añadir_cliente(self, cliente):
        self.clientes.append(cliente)